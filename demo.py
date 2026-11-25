"""Run the offline project demonstration on localhost."""

import argparse
import math

import gradio as gr
import pandas as pd
from pandas.api.types import is_integer_dtype

from project_model import CATEGORICAL_COLUMNS, THRESHOLD, load_train, make_forest

RATE_COLUMNS = {"BounceRates", "ExitRates", "SpecialDay"}


def build_demo():
    X, y = load_train()
    forest = make_forest(X.columns).fit(X, y)
    train_scores = forest.predict_proba(X)[:, 1]
    sample_rows = X.iloc[[train_scores.argmin(), train_scores.argmax()]]
    samples = sample_rows.to_dict(orient="split")["data"]

    inputs = []
    for column, initial in zip(X.columns, samples[0]):
        if column in CATEGORICAL_COLUMNS:
            choices = sorted(X[column].dropna().unique().tolist())
            inputs.append(gr.Dropdown(choices=choices, value=initial, label=column))
        else:
            inputs.append(gr.Number(
                value=initial, label=column, minimum=0,
                maximum=1 if column in RATE_COLUMNS else None,
                precision=0 if is_integer_dtype(X[column]) else None,
            ))

    def predict(*values):
        for column, value in zip(X.columns, values):
            if value is None:
                raise gr.Error(f"Hãy nhập giá trị cho {column}.")
            if column not in CATEGORICAL_COLUMNS:
                if not math.isfinite(value) or value < 0:
                    raise gr.Error(f"{column} phải là số hữu hạn không âm.")
                if column in RATE_COLUMNS and value > 1:
                    raise gr.Error(f"{column} phải nằm trong khoảng từ 0 đến 1.")

        row = pd.DataFrame([values], columns=X.columns).astype(X.dtypes)
        score = float(forest.predict_proba(row)[0, 1])
        label = "Có mua" if score >= THRESHOLD else "Không mua"
        return label, score

    return gr.Interface(
        fn=predict,
        inputs=inputs,
        outputs=[
            gr.Textbox(label="Nhãn dự đoán"),
            gr.Number(label="Điểm mua (0–1)", precision=6),
        ],
        title="Dự đoán khả năng mua hàng",
        description=(
            "Chọn một phiên mẫu rồi nhấn Submit, hoặc sửa 16 đặc trưng tổng hợp theo phiên. "
            f"Random Forest dùng ngưỡng {THRESHOLD:.5f} để gán nhãn mua. "
            "Điểm mua là đầu ra của mô hình dùng cho minh họa offline."
        ),
        examples=samples,
        cache_examples=False,
        analytics_enabled=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    build_demo().launch(server_name="127.0.0.1", server_port=args.port, share=False)
