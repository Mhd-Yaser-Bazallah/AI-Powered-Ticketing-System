import os
import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fuzzywuzzy import fuzz

class TeamClassifier:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, "models", "bert_ticket_classifier")

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

        encoder_path = os.path.join(base_dir, "models", "bert_label_encoder.joblib")
        self.label_encoder = joblib.load(encoder_path)

    def predict_raw(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=96
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0]
        class_id = torch.argmax(probs).item()
        confidence = float(probs[class_id])

        category = self.label_encoder.inverse_transform([class_id])[0]
        return category, confidence

    def match_team_to_company(self, predicted_category, company_teams):
        for team in company_teams:
            if team.lower() == predicted_category.lower():
                return team, False

        best_team = None
        best_score = 0

        for team in company_teams:
            score = fuzz.ratio(team.lower(), predicted_category.lower())
            if score > best_score:
                best_score = score
                best_team = team

        if best_score >= 70:
            return best_team, False

        return None, True

    def classify_ticket(self, text, company_teams):
        predicted_category, confidence = self.predict_raw(text)

        matched_team, need_admin = self.match_team_to_company(
            predicted_category, company_teams
        )

        return {
            "predicted_category": predicted_category,
            "matched_team": matched_team,
            "need_admin": need_admin,
            "confidence": confidence
        }
