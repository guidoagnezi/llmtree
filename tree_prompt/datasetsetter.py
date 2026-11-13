import pandas as pd
from pathlib import Path

df = pd.read_csv("The clinical laboratory data of bladder cancer .csv", dtype=str)

df = df.drop(columns=["Patient Number"])

label_map = {
    "Cystitis": "0",
    "Kidney": "1",
    "Prostate": "2",
    "UrinaryBladder": "3",
    "Uterus": "4",
}
df["Disease"] = df["Disease"].map(label_map)

Path("dataset/bladder").mkdir(parents=True, exist_ok=True)
df.to_csv("dataset/bladder/data.csv", index=False)