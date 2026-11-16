from transformers import pipeline
from datasets import load_dataset
from sklearn.metrics import accuracy_score, classification_report
 
# device=0 uses GPU if available; remove this arg to run on CPU
sentiment_model = pipeline("sentiment-analysis", device=0)
 
dataset = load_dataset("fancyzhx/yelp_polarity", split="test[:500]")
 
# Result from actual run (500-sample test split):
# Accuracy: 85.40%
#               precision    recall  f1-score   support
#     Negative       0.86      0.85      0.85       250
#     Positive       0.85      0.86      0.85       250
#     accuracy                           0.85       500
 
true_labels = []
pred_labels = []
 
for example in dataset:
    text = example["text"][:512]  # truncate to model's max input length
    true_label = example["label"]  # 0 = negative, 1 = positive
 
    result = sentiment_model(text)[0]
    pred_label = 1 if result["label"] == "POSITIVE" else 0
 
    true_labels.append(true_label)
    pred_labels.append(pred_label)
 
accuracy = accuracy_score(true_labels, pred_labels)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(classification_report(true_labels, pred_labels, target_names=["Negative", "Positive"]))