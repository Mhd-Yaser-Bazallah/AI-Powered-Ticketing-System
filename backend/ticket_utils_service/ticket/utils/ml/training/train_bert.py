import os
import numpy as np
import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.cuda.amp import autocast, GradScaler

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from transformers import AutoTokenizer, AutoModelForSequenceClassification



class TicketsDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=96):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])

        enc = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )

        item = {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long),
        }
        return item



def load_data():
    train_df = pd.read_csv("tickets_train.csv")
    test_df  = pd.read_csv("tickets_test.csv")

    train_df = train_df.dropna(subset=["Document", "Topic_group"])
    test_df  = test_df.dropna(subset=["Document", "Topic_group"])

    return train_df, test_df


train_df, test_df = load_data()

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(train_df["Topic_group"])
y_test  = label_encoder.transform(test_df["Topic_group"])

X_train = train_df["Document"].tolist()
X_test  = test_df["Document"].tolist()

num_labels = len(label_encoder.classes_)
joblib.dump(label_encoder, "bert_label_encoder.joblib")



MODEL_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels,
)

device = torch.device("cuda")
model.to(device)

scaler = GradScaler()



train_dataset = TicketsDataset(X_train, y_train, tokenizer, max_length=96)
test_dataset  = TicketsDataset(X_test,  y_test,  tokenizer, max_length=96)

train_loader = DataLoader(train_dataset, batch_size=24, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=48, shuffle=False)



optimizer = AdamW(model.parameters(), lr=2e-5)
num_epochs = 3

for epoch in range(1, num_epochs + 1):
    model.train()
    total_loss = 0.0

    for batch in train_loader:
        input_ids      = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels         = batch["labels"].to(device)

        optimizer.zero_grad()

        with autocast():
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
            )
            loss = outputs.loss

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()

    avg_train_loss = total_loss / len(train_loader)

    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in test_loader:
            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels         = batch["labels"].to(device)

            with autocast():
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                )

            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1)

            all_preds.extend(preds.cpu().numpy().tolist())
            all_labels.extend(labels.cpu().numpy().tolist())

    acc         = accuracy_score(all_labels, all_preds)
    f1_macro    = f1_score(all_labels, all_preds, average="macro")
    f1_weighted = f1_score(all_labels, all_preds, average="weighted")




report = classification_report(
    all_labels, all_preds,
    target_names=label_encoder.classes_,
    digits=3,
)

accuracy     = accuracy_score(all_labels, all_preds)
f1_macro     = f1_score(all_labels, all_preds, average="macro")
f1_weighted  = f1_score(all_labels, all_preds, average="weighted")


cm = confusion_matrix(all_labels, all_preds)
labels = list(label_encoder.classes_)

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix - BERT")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.savefig("bert_confusion_matrix.png")

with open("bert_results.txt", "w", encoding="utf-8") as f:
    f.write("===== BERT RESULTS =====\n")
    f.write(f"Acc: {accuracy}\n")
    f.write(f"F1 Macro: {f1_macro}\n")
    f.write(f"F1 Weighted: {f1_weighted}\n\n")
    f.write(report)

model.save_pretrained("bert_ticket_classifier")
tokenizer.save_pretrained("bert_ticket_classifier")

