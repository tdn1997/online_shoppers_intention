"""Load the fixed training split and build the Random Forest from week 3."""

from hashlib import sha256
import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent
THRESHOLD = 0.20964924233624288
CATEGORICAL_COLUMNS = [
    "Month", "OperatingSystems", "Browser", "Region",
    "TrafficType", "VisitorType", "Weekend",
]


def load_train():
    csv = ROOT / "data" / "online_shoppers_intention.csv"
    split_path = ROOT / "data" / "split_indices.json"
    split = json.loads(split_path.read_text(encoding="utf-8"))
    if sha256(csv.read_bytes()).hexdigest() != split["csv_sha256"]:
        raise ValueError("CSV không khớp với split đã lưu.")

    df = pd.read_csv(csv)
    train_indices = split["train_indices"]
    all_indices = train_indices + split["test_indices"]
    if (
        len(all_indices) != len(df)
        or split["n_rows"] != len(df)
        or any(type(index) is not int for index in all_indices)
        or set(all_indices) != set(df.index)
    ):
        raise ValueError("Split phải phủ đủ các dòng và mỗi dòng xuất hiện đúng một lần.")

    train = df.iloc[train_indices]
    return train.drop(columns=["Revenue", "PageValues"]), train["Revenue"]


def make_forest(features):
    numeric = [column for column in features if column not in CATEGORICAL_COLUMNS]
    preprocessing = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False),
         CATEGORICAL_COLUMNS),
        ("numeric", "passthrough", numeric),
    ])
    return Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", RandomForestClassifier(
            n_estimators=100, max_depth=12, min_samples_leaf=5,
            random_state=42, n_jobs=1,
        )),
    ])
