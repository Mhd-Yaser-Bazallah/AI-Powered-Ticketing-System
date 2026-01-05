                                       

import os

from sentence_transformers import SentenceTransformer
from ticket.models import Team

model_path = os.getenv("TEAM_EMBEDDING_MODEL_PATH") or "all-MiniLM-L6-v2"
embed_model = SentenceTransformer(model_path, local_files_only=True)

def update_team_embedding(team: Team):
    text = f"{team.category}. {team.description}"
    vec = embed_model.encode(text, normalize_embeddings=True)
    team.embedding = vec.tolist()
    team.save(update_fields=["embedding"])



                                
                             
