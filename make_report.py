# make_report.py
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
fin_csv = ROOT / "results" / "finetune_results.csv"
rag_csv = ROOT / "results" / "rag_results.csv"
summary_txt = ROOT / "results" / "comparison_summary.txt"
out_md = ROOT / "results" / "report.md"

assert fin_csv.exists(), f"Нет {fin_csv} — сначала запусти finetune/test.py"
assert rag_csv.exists(), f"Нет {rag_csv} — сначала запусти rag/test.py"
assert summary_txt.exists(), f"Нет {summary_txt} — сначала запусти compare.py"

df_ft = pd.read_csv(fin_csv)
df_rag = pd.read_csv(rag_csv)
df = df_ft.merge(df_rag, on="question", how="inner", suffixes=("_ft", "_rag"))

summary = Path(summary_txt).read_text(encoding="utf-8")


# делаем красивую таблицу в md
def to_md_table(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False)


body = f"""# Отчёт: Fine-tuning vs RAG (Университет ИИ)

## 1. Датасет
Использован единый датасет `data/uai_dataset.csv` (+ автогенерация `ft_train.jsonl` и `rag_corpus.csv`).

## 2. Тестовые вопросы (5 шт.)
1. Нужен ли опыт программирования для поступления в УИИ?
2. Сколько времени занимает обучение каждую неделю и есть ли лайв-сессии?
3. Что выбрать: RAG или fine-tuning, если база знаний часто обновляется?
4. Помогаете ли вы с трудоустройством и как это устроено?
5. Есть ли платные интенсивы, чтобы быстро стартовать, и что посоветуете?

## 3. Ответы моделей
Ниже — сравнение ответов fine-tuned модели и RAG на одних и тех же вопросах.

{to_md_table(df[["question", "answer_ft", "answer_rag"]])}

## 4. Сводка метрик и вывод
{summary}

## 5. Замечания по целям (upsell/мотивация)
— В датасете и промптах добавлена ссылка: https://neural-university.ru/
— Модель обучена мягко предлагать платные интенсивы/курсы, CTA добавляется по контексту.

"""

out_md.write_text(body, encoding="utf-8")
print(f"✅ Готово: {out_md}")
