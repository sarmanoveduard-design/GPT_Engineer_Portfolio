from __future__ import annotations

import csv
from pathlib import Path

from rag.pipeline import generate_answer

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

QUESTIONS = [
    "Нужен ли опыт программирования для поступления в УИИ?",
    "Сколько времени занимает обучение каждую неделю и есть ли лайв-сессии?",
    "Что выбрать: RAG или fine-tuning, если база знаний часто обновляется?",
    "Помогаете ли вы с трудоустройством и как это устроено?",
    "Есть ли платные интенсивы, чтобы быстро стартовать, и что посоветуете?",
]


def main() -> None:
    out_csv = RESULTS / "rag_results.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer"])
        for q in QUESTIONS:
            a = generate_answer(q)
            writer.writerow([q, a])
    print("✅ Сохранено:", out_csv)


if __name__ == "__main__":
    main()
