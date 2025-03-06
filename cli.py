# pubmed_fetcher/cli.py
import argparse
from pubmed_fetcher.fetch import fetch_papers, save_to_csv

def main():
    """
    Command-line interface for fetching PubMed papers.
    
    Parses command-line arguments, fetches research papers from PubMed based on a search query,
    and either prints the results to the console or saves them to a CSV file.
    """
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Fetch research papers based on user query
    papers = fetch_papers(args.query)
    
    if args.file:
        # Save results to a CSV file if specified
        save_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        # Print results to console
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
