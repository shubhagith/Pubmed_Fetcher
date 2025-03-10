# PubMed Fetcher

## Overview
PubMed Fetcher is a Python-based tool that retrieves research papers from PubMed using the Entrez Programming Utilities (E-utilities) API. It allows users to search for articles based on a given query and extract key details such as title, publication date, author affiliations, and corresponding author email. The fetched data can be saved into a CSV file.

## Project Structure
```
pubmed_fetcher/
│-- __init__.py  # Marks the directory as a package
│-- fetch.py     # Handles fetching, processing, and saving paper details
│-- cli.py       # Command-line interface for fetching and saving data
│-- README.md    # Documentation
```

## Installation
### Prerequisites
- Python 3.7 or higher
- `requests` library (for making HTTP requests)

### Install Poetry and Dependencies
```sh
pip install poetry
poetry install
```

## Usage

### Command-line Interface
To fetch research papers, run the following command:
```sh
poetry run get-papers-list "cancer treatment"
```

To save the results to a CSV file:
```sh
poetry run get-papers-list "cancer treatment" -f results.csv
```

Enable debug mode for detailed logging:
```sh
poetry run get-papers-list "cancer treatment" -d
```

## Example Output
When running the script without saving to a file, it prints output similar to:
```json
[
  {
    "PubmedID": "12345678",
    "Title": "Recent Advances in Cancer Research",
    "Publication Date": "2023-10-05",
    "Non-academic Author(s)": "John Doe, XYZ Biotech Inc.",
    "Company Affiliation(s)": "XYZ Biotech Inc.",
    "Corresponding Author Email": "johndoe@example.com"
  }
]
```

## API Details
- Uses PubMed's `esearch.fcgi` API to search for article IDs
- Uses `esummary.fcgi` API to fetch detailed metadata

## Notes
- The tool currently fetches up to 10 results (modifiable in `fetch.py`).
- Identifies non-academic affiliations using keyword matching.
- Includes error handling for API failures and invalid queries.

## License
This project is licensed under the MIT License.

