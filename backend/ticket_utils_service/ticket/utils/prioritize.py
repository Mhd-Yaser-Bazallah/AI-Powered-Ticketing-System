import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_sm")

if "spacytextblob" not in nlp.pipe_names:
    nlp.add_pipe("spacytextblob", last=True)

def determine_ticket_priority(description: str) -> str:
    doc = nlp(description)

    if not doc.has_extension("blob"):
        return "medium"

    polarity = doc._.blob.polarity

    if polarity < -0.3:
        return "high"
    elif -0.3 <= polarity < 0.3:
        return "medium"
    else:
        return "low"
 
