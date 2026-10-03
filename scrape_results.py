"""Parse local athletics HTML pages and verify persisted results. Run from project root."""

from pathlib import Path
import scrapy

all_results = []
file_counts = {}

def get_text(element):
    return " ".join(
        " ".join(element.xpath(".//text()").getall()).split()
    )

for file_path in sorted(Path("html").iterdir()):
    if not file_path.is_file():
        continue

    html_data = file_path.read_text(encoding="utf-8")

    page = scrapy.http.TextResponse(
        url=file_path.resolve().as_uri(),
        body=html_data,
        encoding="utf-8"
    )

    file_counts[file_path.name] = 0

    for table_index, html_table in enumerate(page.xpath("//table")):
        table_rows = html_table.xpath(".//tr")

        if not table_rows:
            continue

        headers = [
            get_text(cell).lower()
            for cell in table_rows[0].xpath("./th | ./td")
        ]

        required = ["rank", "name", "nationality", "result"]

        if not all(column in headers for column in required):
            continue

        for tr in table_rows[1:]:
            cells = tr.xpath("./th | ./td")

            if len(cells) < len(headers):
                continue

            values = [get_text(cell) for cell in cells]

            rank_cell = cells[headers.index("rank")]
            rank = values[headers.index("rank")]

            # Medal ranks may appear as images instead of text.
            if not rank:
                rank = rank_cell.xpath(".//img/@alt").get() or ""

            athlete = values[headers.index("name")]
            country = values[headers.index("nationality")]
            result = values[headers.index("result")]

            notes = (
                values[headers.index("notes")]
                if "notes" in headers
                else ""
            )

            if not athlete:
                continue

            all_results.append({
                "source_file": file_path.name,
                "table_index": table_index,
                "rank": rank,
                "athlete": athlete,
                "nationality": country,
                "result": result,
                "notes": notes
            })

            file_counts[file_path.name] += 1

for filename, count in file_counts.items():
    print(f"{filename}: {count} results")

print(f"\nTotal: {len(all_results)} results")

assert all_results, "No results found."
assert all(file_counts.values()), "A file had no matching results."

import json
import csv

with open("all_results.json", "w", encoding="utf-8") as file:
    json.dump(all_results, file, indent=4, ensure_ascii=False)

column_names = [
    "source_file",
    "table_index",
    "rank",
    "athlete",
    "nationality",
    "result",
    "notes"
]

with open(
    "all_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.DictWriter(file, fieldnames=column_names)
    writer.writeheader()
    writer.writerows(all_results)

print("JSON and CSV saved.")

import sqlite3

connection = sqlite3.connect("all_results.db")

try:
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                source_file TEXT,
                table_index INTEGER,
                rank TEXT,
                athlete TEXT,
                nationality TEXT,
                result TEXT,
                notes TEXT
            )
        """)

        connection.execute("DELETE FROM results")

        connection.executemany("""
            INSERT INTO results (
                source_file, table_index, rank, athlete,
                nationality, result, notes
            )
            VALUES (
                :source_file, :table_index, :rank, :athlete,
                :nationality, :result, :notes
            )
        """, all_results)

finally:
    connection.close()

print(f"Saved {len(all_results)} results to SQLite.")

connection = sqlite3.connect("all_results.db")
connection.row_factory = sqlite3.Row

try:
    saved_results = [
        dict(row)
        for row in connection.execute("""
            SELECT source_file, table_index, rank, athlete,
                   nationality, result, notes
            FROM results
            ORDER BY id
        """)
    ]
finally:
    connection.close()

assert saved_results == all_results, "Saved data does not match."

print(f"Verified: all {len(saved_results)} results match.")

for row in saved_results[:10]:
    print(row)
