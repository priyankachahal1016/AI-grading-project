import os
import pandas as pd

os.makedirs("outputs", exist_ok=True)

# 1. Load your dataset (change filename to 'data/train.tsv' if using that file)
df = pd.read_csv("data/train_rel_2.tsv", sep="\t", encoding="ISO-8859-1")

# 2. Randomly pick 30 answers from Set 1 and 30 from Set 3 (fixed random_state so it's reproducible)
s1_sample = df[df["EssaySet"] == 1].sample(n=30, random_state=101)
s3_sample = df[df["EssaySet"] == 3].sample(n=30, random_state=101)

combined = pd.concat([s1_sample, s3_sample]).reset_index(drop=True)

# 3. Save the secret answer key (keep closed until you finish grading!)
combined[["Id", "EssaySet", "Score1", "Score2"]].to_excel(
    "outputs/blind_answer_key.xlsx", index=False
)

# 4. Save the blind grading sheet for you to fill out
blind_sheet = combined[["Id", "EssaySet", "EssayText"]].copy()
blind_sheet["MyScore"] = ""
blind_sheet["Notes"] = ""
blind_sheet.to_excel("outputs/blind_grading_sheet.xlsx", index=False)

print("Done! Open 'outputs/blind_grading_sheet.xlsx' to start grading.")