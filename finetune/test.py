from __future__ import annotations

import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# читаем модель: сначала .env, потом fallback в results/ft_model.txt
ft_model = os.getenv("FT_MODEL")
if not ft_model:
    ft_file = RESULTS / "ft_model.txt"
    if ft_file.exists():
        ft_model = ft_file.read_text(encoding="utf-8").strip()

assert (
    ft_model
), "Не задан FT_MODEL (в .env) и нет results/ft_model.txt — нечем тестировать"

SYSTEM = (
    "Ты — ассистент УИИ. Отвечай чётко, дружелюбно, с кратким планом и мягким CTA "
    "на платные курсы, если уместно."
)

QUESTIONS = [
    "Нужен ли опыт программирования для поступления в УИИ?",
    "Сколько времени занимает обучение каждую неделю и есть ли лайв-сессии?",
    "Что выбрать: RAG или fine-tuning, если база знаний часто обновляется?",
    "Помогаете ли вы с трудоустройством и как это устроено?",
    "Есть ли платные интенсивы, чтобы быстро стартовать, и что посоветуете?",
]


def ask(q: str) -> str:
    resp = client.chat.completions.create(
        model=ft_model,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


def main() -> None:
    out_csv = RESULTS / "finetune_results.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer"])
        for q in QUESTIONS:
            a = ask(q)
            writer.writerow([q, a])
    print("✅ Сохранено:", out_csv)


if __name__ == "__main__":
    main()
