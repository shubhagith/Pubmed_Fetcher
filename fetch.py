# pubmed_fetcher/fetch.py
import requests
import csv
import re
import logging
from typing import List, Dict, Tuple, Optional

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_papers(query: str) -> List[Dict[str, Optional[str]]]:
    """
    Fetch research papers from PubMed based on the given query.
    
    Args:
        query (str): The search term for retrieving PubMed articles.
    
    Returns:
        List[Dict[str, Optional[str]]]: A list of dictionaries containing paper details.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Fetch up to 10 articles for testing
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        pubmed_ids = data.get("esearchresult", {}).get("idlist", [])
        logging.info(f"Fetched {len(pubmed_ids)} papers.")
        return get_paper_details(pubmed_ids)
    except requests.RequestException as e:
        logging.error(f"Error fetching data from PubMed: {e}")
        return []

def get_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Optional[str]]]:
    """
    Fetch detailed information for a list of PubMed article IDs.
    
    Args:
        pubmed_ids (List[str]): A list of PubMed article IDs.
    
    Returns:
        List[Dict[str, Optional[str]]]: A list of dictionaries containing paper details.
    """
    if not pubmed_ids:
        logging.warning("No PubMed IDs found for the given query.")
        return []
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        details = response.json().get("result", {})
        
        papers = []
        for pmid in pubmed_ids:
            if pmid in details:
                paper_info = details[pmid]
                authors, companies, email = extract_affiliations(paper_info)
                papers.append({
                    "PubmedID": pmid,
                    "Title": paper_info.get("title", "N/A"),
                    "Publication Date": paper_info.get("pubdate", "N/A"),
                    "Non-academic Author(s)": authors,
                    "Company Affiliation(s)": companies,
                    "Corresponding Author Email": email
                })
        logging.info(f"Retrieved details for {len(papers)} papers.")
        return papers
    except requests.RequestException as e:
        logging.error(f"Error fetching paper details from PubMed: {e}")
        return []

def extract_affiliations(paper_info: Dict) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract non-academic author names, company affiliations, and corresponding author email.
    
    Args:
        paper_info (Dict): A dictionary containing paper details from PubMed.
    
    Returns:
        Tuple[Optional[str], Optional[str], Optional[str]]: Non-academic authors, company affiliations, and email.
    """
    affiliations = paper_info.get("affiliations", [])
    non_academic_authors = []
    company_affiliations = []
    corresponding_email: Optional[str] = "N/A"
    
    for aff in affiliations:
        # Identify non-academic affiliations based on keywords
        if any(keyword in aff.lower() for keyword in ["pharma", "biotech", "inc.", "ltd.", "corporation", "gmbh"]):
            non_academic_authors.append(aff)
            company_affiliations.append(aff)
    
    if "author_email" in paper_info:
        corresponding_email = paper_info.get("author_email", "N/A")
    
    return ", ".join(non_academic_authors) or None, ", ".join(company_affiliations) or None, corresponding_email

def save_to_csv(papers: List[Dict[str, Optional[str]]], filename: str):
    """
    Save the fetched papers to a CSV file.
    
    Args:
        papers (List[Dict[str, Optional[str]]]): List of paper details to be saved.
        filename (str): The name of the output CSV file.
    """
    if not papers:
        logging.warning("No data to save to CSV.")
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)
    logging.info(f"Results saved to {filename}")
