# Athletics Results Scraper

A Python learning project by **Cesar Sierra** that extracts men’s high-jump results from saved Wikipedia HTML pages and persists them as JSON, CSV, and SQLite.

Built while completing a Coursera guided project taught by **Alfredo Deza**. The notebook includes the original single-page medal example and an extension that processes four pages and qualifying/final results. Developed with AI-assisted coding and debugging.

## What it does

- Reads local HTML files without making network requests.
- Uses Scrapy’s HTML selectors and XPath to locate tables by column headings.
- Extracts rank, athlete, nationality, jump result, and notes.
- Preserves the source filename and table index for each performance.
- Writes JSON, CSV, and a SQLite database.
- Opens a fresh database connection and compares every saved record with the extracted data.

## Recorded results

The supplied course pages produced the following counts in the original notebook run:

| Competition year | Performance records |
| --- | ---: |
| 1992 | 51 |
| 1994 | 43 |
| 1996 | 46 |
| 1998 | 44 |
| **Total** | **184** |

These are performance records, not unique athletes: qualifying and final appearances are separate rows. The original run reported `Verified: all 184 results match.` This verifies persistence, not independent completeness against every source row.

## Files

| File | Purpose |
| --- | --- |
| `persistence.ipynb` | Step-by-step notebook, with outputs cleared for a clean rerun |
| `scrape_results.py` | Standalone version of the all-files parsing and persistence section |
| `requirements.txt` | Python dependencies |
| `html/` | Folder for the course input pages |
| `.gitignore` | Excludes environments, caches, and generated outputs |

**The original HTML pages and generated datasets are not included in this package.** Download the input pages from your course workspace and place them inside `html/`. Delete `html/README.md` before running, because the current parser reads every regular file in that folder.

Required original filenames (no extension):

```text
1992_World_Junior_Championships_in_Athletics_–_Men's_high_jump
1994_World_Junior_Championships_in_Athletics_–_Men's_high_jump
1996_World_Junior_Championships_in_Athletics_–_Men's_high_jump
1998_World_Junior_Championships_in_Athletics_–_Men's_high_jump
```

## Setup and run

Use Python 3.10 or newer. Open a terminal in this project folder.

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the standalone script:

```bash
python scrape_results.py
```

Or start JupyterLab, open `persistence.ipynb`, and run the cells from top to bottom:

```bash
jupyter lab
```

Run from the project root so that `html/` is found. An import error for Scrapy means the selected Python environment lacks the dependency.

## Outputs and database

The all-files section creates `all_results.json`, `all_results.csv`, and `all_results.db` in the working directory. The notebook also produces three `1992_results` files for the initial medal example.

The SQLite `results` table stores an ID plus `source_file`, `table_index`, `rank`, `athlete`, `nationality`, `result`, and `notes`. Rank and result remain text to preserve medal descriptions and nonnumeric statuses. Numeric high-jump results represent meters.

Rerunning persistence replaces the rows in these practice databases. Do not point the code at an unrelated database with valuable records.

## Limitations

- Input files must use the expected table headings and UTF-8 encoding.
- Rows with fewer cells than headers are skipped; merged cells may require additional handling.
- Table indices identify source tables but do not explicitly label final versus qualifying rounds.
- All extracted rows are accumulated in memory before persistence.
- The supplied input pages are required to reproduce the recorded 184-row run.

The duplicate insertion cell from the earlier notebook was removed. The packaged Python cells and script were checked for syntax; the full data run was not repeated during packaging because the HTML files were unavailable.

## Credits and source data

Course instructor: Alfredo Deza. Related course: [Scripting with Python and SQL for Data Engineering](https://www.coursera.org/learn/scripting-with-python-sql-for-data-engineering-duke).

Source pages: Wikipedia articles titled “1992/1994/1996/1998 World Junior Championships in Athletics – Men’s high jump.” If you publish copies of the HTML or data, include their exact source URLs, retrieval dates when known, and applicable source attribution/license notices. This package does not assign a license to course material or Wikipedia content.

## Publish on GitHub

1. Extract this ZIP.
2. Create a repository named `athletics-results-scraper`.
3. Upload the contents of the extracted project folder, including `.gitignore`.
4. Add course input files only after checking their redistribution terms; otherwise document how to obtain them.
5. Suggested description: “Python project extracting athletics results from local HTML and saving verified records to JSON, CSV, and SQLite.”
