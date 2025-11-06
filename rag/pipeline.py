from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DATA = ROOT / "data"
INDEX = DATA / "rag_index.npz"
CORPUS = DATA / "rag_corpus.csv"

EMB_MODEL = "text-embedding-3-small"
GEN_MODEL = "gpt-4o-mini-2024-07-18"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_corpus() -> Tuple[List[str], List[str]]:
    ids: List[str] = []
    texts: List[str] = []
    with CORPUS.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(row["doc_id"])
            texts.append(row["text"])
    return ids, texts


def build_index():
    ids, texts = load_corpus()
    embs = []
    for t in texts:
        e = client.embeddings.create(model=EMB_MODEL, input=t).data[0].embedding
        embs.append(e)
    arr = np.array(embs, dtype=np.float32)
    np.savez_compressed(INDEX, ids=np.array(ids), embs=arr)
    return ids, arr


def load_index():
    if not INDEX.exists():
        return build_index()
    z = np.load(INDEX, allow_pickle=True)
    return z["ids"].tolist(), z["embs"]


def search(query: str, top_k: int = 4) -> List[str]:
    ids, embs = load_index()
    q_emb = client.embeddings.create(model=EMB_MODEL, input=query).data[0].embedding
    q = np.array(q_emb, dtype=np.float32)
    norms = np.linalg.norm(embs, axis=1) * (np.linalg.norm(q) + 1e-12)
    sims = (embs @ q) / (norms + 1e-12)
    top_idx = sims.argsort()[-top_k:][::-1]
    _, texts = load_corpus()
    return [texts[i] for i in top_idx]


SALES_STYLE = (
    "Ты — ассистент УИИ. Коротко и по делу. Используй предоставленный контекст. "
    "В конце добавь мягкий CTA (одно предложение) с приглашением на интенсив/курс, если уместно."
)


def generate_answer(question: str) -> str:
    ctx_snippets = search(question, top_k=4)
    context = "\n\n---\n".join(ctx_snippets)
    prompt = (
        "Контекст (фрагменты базы знаний УИИ):\n"
        f"{context}\n\n"
        f"Вопрос пользователя: {question}\n"
        "Ответь строго на основе контекста."
    )
    resp = client.chat.completions.create(
        model=GEN_MODEL,
        messages=[{"role": "system", "content": SALES_STYLE}, {"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
