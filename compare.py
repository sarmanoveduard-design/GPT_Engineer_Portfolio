# compare.py
from __future__ import annotations
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
fin_csv = ROOT / "results" / "finetune_results.csv"
rag_csv = ROOT / "results" / "rag_results.csv"

assert fin_csv.exists(), f"Нет файла {fin_csv}. Сначала запусти finetune/test.py"
assert rag_csv.exists(), f"Нет файла {rag_csv}. Сначала запусти rag/test.py"

df_ft = pd.read_csv(fin_csv)
df_rag = pd.read_csv(rag_csv)

# Соединяем по вопросу
df = df_ft.merge(df_rag, on="question", how="inner", suffixes=("_ft", "_rag"))


# Простая «оценка выполнения цели» (эвристики):
# - наличие upsell/CTA (по ключевым фразам)
# - структурированность (наличие списков/переносов)
def score_cta(text: str) -> int:
    text = (text or "").lower()
    keys = ["интенсив", "курс", "присоедин", "подроб", "neural-university.ru", "ссылка", "оформить"]
    return int(any(k in text for k in keys))


def score_structure(text: str) -> int:
    t = text or ""
    bullets = sum(t.count(x) for x in ["- ", "•", "1.", "2.", "3."])
    newlines = t.count("\n")
    return int(bullets > 0 or newlines >= 2)


def score_precision(text: str) -> int:
    # эвристика: чем меньше «воды», тем лучше (<= 600 символов, и нет "как искусственный интеллект..." и т.д.)
    t = (text or "")
    penalties = ["как искусственный интеллект", "не имею доступа", "не могу просматривать"]
    bad = any(p in t.lower() for p in penalties)
    return int((len(t) <= 600) and not bad)


for col in ["answer_ft", "answer_rag"]:
    df[f"{col}_cta"] = df[col].map(score_cta)
    df[f"{col}_struct"] = df[col].map(score_structure)
    df[f"{col}_prec"] = df[col].map(score_precision)
    df[f"{col}_score"] = df[f"{col}_cta"] + df[f"{col}_struct"] + df[f"{col}_prec"]

# Итоговые метрики по каждому подходу
summary = pd.DataFrame({
    "metric": ["CTA (есть мягкая продажа)", "Структура (списки/переносы)", "Краткость/точность (эвристика)", "Суммарный балл"],
    "fine_tune": [
        df["answer_ft_cta"].mean(),
        df["answer_ft_struct"].mean(),
        df["answer_ft_prec"].mean(),
        df["answer_ft_score"].mean(),
    ],
    "rag": [
        df["answer_rag_cta"].mean(),
        df["answer_rag_struct"].mean(),
        df["answer_rag_prec"].mean(),
        df["answer_rag_score"].mean(),
    ],
}).round(2)

# Выводим
print("\n=== Fine-tune vs RAG: ответы по вопросам ===")
print(df[["question", "answer_ft", "answer_rag"]].to_string(index=False))

print("\n=== Сводка метрик (0..1/0..3) ===")
print(summary.to_string(index=False))

# Текстовый вывод-рекомендация
ft_total = summary.loc[summary["metric"] == "Суммарный балл", "fine_tune"].iloc[0]
rag_total = summary.loc[summary["metric"] == "Суммарный балл", "rag"].iloc[0]

if ft_total > rag_total + 0.2:
    verdict = "Победил **Fine-tuning**: стиль и CTA стабильнее, ответы короче и “бренд-консистентнее”."
elif rag_total > ft_total + 0.2:
    verdict = "Победил **RAG**: выше точность по базе знаний и уместные CTA из контекста."
else:
    verdict = "Ничья по сумме: рекомендуем **комбинировать** — FT для стиля/CTA, RAG для свежих фактов."

print("\n=== Вывод ===")
print(verdict)

# Сохраним отчёт
OUT = ROOT / "results" / "comparison_summary.txt"
with OUT.open("w", encoding="utf-8") as f:
    f.write("== Fine-tune vs RAG ==\n\n")
    f.write(summary.to_string(index=False))
    f.write("\n\n" + verdict + "\n")
print(f"\n📝 Отчёт сохранён: {OUT}")
