from collections import Counter
from io import StringIO
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXPORT_DIR = Path(__file__).resolve().parents[1] / "static" / "charts"

def to_frame(rows):
    columns = ["course_name", "question_text", "rating", "submitted_at"]
    df = pd.DataFrame(rows, columns=columns)
    if not df.empty:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df = df.dropna(subset=["rating"])
    return df

def build_summary(rows):
    df = to_frame(rows)
    if df.empty:
        return {"overall_average": None, "total_responses": 0,
                "courses": [], "distributions": []}

    course_stats = []
    for course, group in df.groupby("course_name"):
        course_stats.append({
            "course_name": course,
            "average": round(float(np.mean(group["rating"].to_numpy())), 2),
            "responses": int(group["rating"].count())
        })

    question_stats = []
    for question, group in df.groupby("question_text"):
        question_stats.append({
            "question_text": question,
            "average": round(float(np.mean(group["rating"].to_numpy())), 2),
            "responses": int(group["rating"].count())
        })

    distribution = []
    counts = df["rating"].value_counts().reindex([1,2,3,4,5], fill_value=0)
    for rating, count in counts.items():
        distribution.append({"rating": int(rating), "count": int(count)})

    return {
        "overall_average": round(float(np.mean(df["rating"].to_numpy())), 2),
        "total_responses": int(df["rating"].count()),
        "courses": course_stats,
        "questions": question_stats,
        "distributions": distribution
    }

def create_charts(rows):
    EXPORT_DIR.mkdir(exist_ok=True)
    df = to_frame(rows)
    if df.empty:
        for name in ("rating_distribution.png", "course_comparison.png"):
            path = EXPORT_DIR / name
            if path.exists():
                path.unlink()
        return

    counts = df["rating"].value_counts().reindex([1,2,3,4,5], fill_value=0)
    plt.figure(figsize=(7, 4))
    counts.plot(kind="bar")
    plt.title("Feedback Rating Distribution")
    plt.xlabel("Rating (1–5)")
    plt.ylabel("Number of responses")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(EXPORT_DIR / "rating_distribution.png")
    plt.close()

    averages = df.groupby("course_name")["rating"].mean().sort_values()
    plt.figure(figsize=(8, 4))
    averages.plot(kind="bar")
    plt.title("Average Rating by Course")
    plt.xlabel("Course")
    plt.ylabel("Average rating")
    plt.ylim(0, 5)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(EXPORT_DIR / "course_comparison.png")
    plt.close()

def summary_csv(rows):
    summary = build_summary(rows)
    output = StringIO()
    pd.DataFrame(summary["courses"]).to_csv(output, index=False)
    return output.getvalue()
