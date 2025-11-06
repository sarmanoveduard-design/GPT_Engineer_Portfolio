from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TRAIN_FILE = DATA / "ft_train.jsonl"
BASE_MODEL = "gpt-4o-mini-2024-07-18"


def main() -> None:
    assert TRAIN_FILE.exists(), f"Нет файла для обучения: {TRAIN_FILE}"

    # 1) Upload
    uploaded = client.files.create(file=TRAIN_FILE.open("rb"), purpose="fine-tune")
    print("📤 Uploaded file:", uploaded.id)

    # 2) Create FT job
    job = client.fine_tuning.jobs.create(
        training_file=uploaded.id,
        model=BASE_MODEL,
        suffix="uai-sales-style",
    )
    print("🚀 Started fine-tune job:", job.id)

    # 3) Wait until completion (можно прервать и проверять потом)
    print("⏳ Ждём завершения...")
    status = job.status
    while status not in ("succeeded", "failed", "cancelled"):
        time.sleep(10)
        job = client.fine_tuning.jobs.retrieve(job.id)
        status = job.status
        print("   Status:", status)

    if status == "succeeded":
        ft_model = job.fine_tuned_model
        print("✅ Fine-tune готов! Модель:", ft_model)
        (RESULTS / "ft_model.txt").write_text(ft_model or "", encoding="utf-8")
        print("📝 Записал ID в results/ft_model.txt — добавь его в .env как FT_MODEL.")
    else:
        print("❌ Fine-tune завершился со статусом:", status)


if __name__ == "__main__":
    main()
