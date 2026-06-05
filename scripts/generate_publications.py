from pathlib import Path
import csv


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "academic-data" / "publications.csv"
OUTPUT = ROOT / "content" / "publications.md"


def clean(value: str) -> str:
    return (value or "").strip()


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f"Could not find {INPUT}")

    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    def sort_key(row):
        year = clean(row.get("year", "0"))
        return int(year) if year.isdigit() else 0

    rows.sort(key=sort_key, reverse=True)

    lines = [
        "---",
        'title: "Publications"',
        'subtitle: "Selected papers, preprints, and working papers"',
        "---",
        "",
    ]

    current_year = None

    for row in rows:
        year = clean(row.get("year"))
        title = clean(row.get("title"))
        authors = clean(row.get("authors")).replace(";", ",")
        venue = clean(row.get("venue"))
        url = clean(row.get("url"))

        if year != current_year:
            lines.append(f"## {year}")
            lines.append("")
            current_year = year

        item = f"- **{title}**. {authors}."
        if venue:
            item += f" *{venue}*."
        if url:
            item += f" [Link]({url})."

        lines.append(item)
        lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
