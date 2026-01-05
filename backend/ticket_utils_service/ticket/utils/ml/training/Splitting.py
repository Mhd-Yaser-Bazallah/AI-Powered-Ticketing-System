import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("all_tickets_processed_improved_v3.csv", encoding="utf-8")

df = df.dropna(subset=["Document", "Topic_group"])

train_df, test_df = train_test_split(
    df,
    test_size=0.3,
    random_state=42,
    stratify=df["Topic_group"]
)


train_df.to_csv("tickets_train.csv", index=False)
test_df.to_csv("tickets_test.csv", index=False)
