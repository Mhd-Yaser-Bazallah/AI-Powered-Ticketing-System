import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


train_df = pd.read_csv("tickets_train.csv")
test_df = pd.read_csv("tickets_test.csv")

X_train = train_df["Document"]
y_train = train_df["Topic_group"]

X_test = test_df["Document"]
y_test = test_df["Topic_group"]


pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.95,
        sublinear_tf=True,
        strip_accents="unicode"
    )),
    ("clf", LinearSVC())
])


pipeline.fit(X_train, y_train)


preds = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, preds)
f1_macro = f1_score(y_test, preds, average="macro")
f1_weighted = f1_score(y_test, preds, average="weighted")
report = classification_report(y_test, preds, digits=3)



cm = confusion_matrix(y_test, preds)
labels = sorted(train_df["Topic_group"].unique())

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix - SVM")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.tight_layout()
plt.savefig("svm_confusion_matrix.png")
plt.close()



with open("svm_results.txt", "w", encoding="utf-8") as f:
    f.write("===== SVM RESULTS =====\n")
    f.write(f"Accuracy: {accuracy}\n")
    f.write(f"F1 Macro: {f1_macro}\n")
    f.write(f"F1 Weighted: {f1_weighted}\n\n")
    f.write("===== Classification Report =====\n")
    f.write(report)



joblib.dump(pipeline, "svm_ticket_classifier.joblib")
