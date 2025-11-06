from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "uai_dataset.csv"
URL = "https://neural-university.ru/"


def main() -> None:
    rows = []
    with CSV.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows = list(r)
        fieldnames = r.fieldnames

    changed = 0
    for row in rows:
        hook = (row.get("upsell_hook") or "").strip()
        if URL not in hook:
            row["upsell_hook"] = f"{hook} Подробнее: {URL}".strip()
            changed += 1

    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"✅ Обновлён {CSV.name}. Добавлено ссылок: {changed}")


if __name__ == "__main__":
    main()
