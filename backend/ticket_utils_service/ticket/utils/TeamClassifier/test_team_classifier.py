from team_classifier import TeamClassifier

classifier = TeamClassifier(model_path="models/team_bert")

test_tickets = [
    "Internet connection drops every few minutes",
    "Received double charge on my last invoice",
    "Application crashes when opening reports",
    "User unable to reset password via portal",
    "Login button unresponsive on mobile",
    "Database backup failed last night",
    "Customer complaining about long waiting times",
    "Help needed to configure email client"
]

for text in test_tickets:
    team = classifier.predict(text)
