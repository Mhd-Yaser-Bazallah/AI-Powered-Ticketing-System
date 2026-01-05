
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class TicketClassifier:
    def __init__(self, model_path=None):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        if model_path:
            self.model = BertForSequenceClassification.from_pretrained(model_path)
        else:
            self.model = BertForSequenceClassification.from_pretrained(
                'bert-base-uncased',
                num_labels=3
            )
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits).item()

        category = {0: "request", 1: "complaint", 2: "feedback"}[predicted_class_id]


        return category
