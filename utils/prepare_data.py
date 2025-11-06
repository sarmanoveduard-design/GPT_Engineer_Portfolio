from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

CSV_PATH = DATA / "uai_dataset.csv"
FT_JSONL = DATA / "ft_train.jsonl"
RAG_CORPUS = DATA / "rag_corpus.csv"

SYSTEM_PROMPT = (
    "Ты — тёплый и понятный академический ассистент Университета искусственного интеллекта. "
    "Отвечай кратко, структурированно и дружелюбно. Если это уместно — мягко предложи платные "
    "интенсивы/курсы (без агрессии), упоминая их по делу."
)


def build_ft_sample(q: str, a: str, upsell: str) -> dict:
    answer = f"{a}\n\nЕсли хотите быстрее продвинуться: {upsell}"
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "assistant", "content": answer.strip()},
        ]
    }


def main() -> None:
    assert CSV_PATH.exists(), f"Не найден файл: {CSV_PATH}"

    # 1) JSONL для fine-tuning
    with CSV_PATH.open("r", encoding="utf-8") as f, FT_JSONL.open(
        "w", encoding="utf-8"
    ) as out:
        reader = csv.DictReader(f)
        rows = list(reader)
        for row in rows:
            sample = build_ft_sample(
                row["question"], row["answer"], row["upsell_hook"]
            )
            out.write(json.dumps(sample, ensure_ascii=False) + "\n")

    # 2) Корпус для RAG
    with RAG_CORPUS.open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["doc_id", "topic", "text"])
        for r in rows:
            text = (
                f"Вопрос: {r['question']}\n"
                f"Ответ: {r['answer']}\n"
                f"Upsell: {r['upsell_hook']}"
            )
            writer.writerow([r["id"], r["topic"], text])

    print("✅ Готово:", FT_JSONL, "и", RAG_CORPUS)


if __name__ == "__main__":
    main()
