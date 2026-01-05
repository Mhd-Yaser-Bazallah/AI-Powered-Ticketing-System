
import os
from typing import Dict, Any, List, Optional

import numpy as np
import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

from ticket.models import Company, Team


BERT_CONF_MIN = 0.5
SIM_MIN       = 0.1


class TicketRouter:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        models_dir = os.path.normpath(os.path.join(base_dir, "..", "models"))
        model_dir = os.path.join(models_dir, "bert_ticket_classifier")

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.bert_model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.bert_model.eval()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.bert_model.to(self.device)

        encoder_path = os.path.join(models_dir, "bert_label_encoder.joblib")
        self.label_encoder = joblib.load(encoder_path)

        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    def _predict_bert(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=96,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.bert_model(**inputs)

        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)[0]
        class_id = torch.argmax(probs).item()
        confidence = float(probs[class_id])
        category = self.label_encoder.inverse_transform([class_id])[0]

        return category, confidence
    def _embed_text(self, text: str) -> np.ndarray:
        return self.embed_model.encode(text, normalize_embeddings=True)

    def _get_company_teams(self, company: Company) -> List[Team]:
        return list(Team.objects.filter(company=company, embedding__isnull=False))

    def _find_best_team(self, ticket_vec: np.ndarray, teams: List[Team]):
        if not teams:
            return None, 0.0

        best_team = None
        best_sim = -1.0

        for team in teams:
            if not team.embedding:
                continue
            team_vec = np.array(team.embedding, dtype=np.float32)
            sim = float(np.dot(ticket_vec, team_vec))
            if sim > best_sim:
                best_sim = sim
                best_team = team

        if best_team is None:
            return None, 0.0

        return best_team, best_sim
    
    def route_ticket(self, company: Company, description: str) -> Dict[str, Any]:
        bert_category, bert_conf = self._predict_bert(description)

        ticket_vec = self._embed_text(description)

        teams = self._get_company_teams(company)
        best_team, best_sim = self._find_best_team(ticket_vec, teams)

        assigned_team = None
        need_admin = False

        if best_team and best_sim >= SIM_MIN:
            assigned_team = best_team
            need_admin = False
        else:
            assigned_team = None
            need_admin = True

        return {
            "assigned_team_id": assigned_team.id if assigned_team else None,
            "need_admin": need_admin,
            "bert_category": bert_category,
            "bert_confidence": bert_conf,
            "similarity_score": best_sim,
        }









router = TicketRouter()
