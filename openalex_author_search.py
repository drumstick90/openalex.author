#!/usr/bin/env python3
"""
OpenAlex Author Search Test Script

This script demonstrates how to search for authors using the OpenAlex API.
It includes basic search, autocomplete, and field-specific search functionality.

OpenAlex API Documentation: https://docs.openalex.org/api-entities/authors/search-authors
"""

import requests
import json
import sys
import argparse
from typing import Dict, List, Optional
from urllib.parse import quote


class OpenAlexAuthorSearch:
    """Class for searching authors using the OpenAlex API."""
    
    BASE_URL = "https://api.openalex.org"
    
    def __init__(self):
        """Initialize the OpenAlex author search client."""
        self.session = requests.Session()
        # Set a user agent as recommended by OpenAlex
        self.session.headers.update({
            'User-Agent': 'OpenAlex Author Search Test Script (mailto:your-email@example.com)'
        })
    
    def search_authors(self, query: str, per_page: int = 25, page: int = 1) -> Dict:
        """
        Search for authors using the basic search functionality.
        
        Args:
            query: The search query (author name)
            per_page: Number of results per page (max 200)
            page: Page number to retrieve
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.BASE_URL}/authors"
        params = {
            'search': query,
            'per-page': per_page,
            'page': page
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching for authors: {e}")
            return {}
    
    def autocomplete_authors(self, query: str) -> Dict:
        """
        Use autocomplete to search for authors (fast type-ahead search).
        
        Args:
            query: The search query (partial author name)
            
        Returns:
            Dictionary containing the autocomplete response
        """
        url = f"{self.BASE_URL}/autocomplete/authors"
        params = {'q': query}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error with autocomplete search: {e}")
            return {}
    
    def search_authors_by_field(self, field: str, query: str, per_page: int = 25) -> Dict:
        """
        Search for authors using field-specific search.
        
        Args:
            field: The field to search in (e.g., 'display_name')
            query: The search query
            per_page: Number of results per page
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.BASE_URL}/authors"
        filter_param = f"{field}.search:{query}"
        params = {
            'filter': filter_param,
            'per-page': per_page
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching authors by field: {e}")
            return {}
    
    def get_author_by_id(self, author_id: str) -> Dict:
        """
        Get a specific author by their OpenAlex ID.
        
        Args:
            author_id: The OpenAlex author ID (e.g., 'A5007433649' or full URL)
            
        Returns:
            Dictionary containing the author data
        """
        # Handle both short ID and full URL formats
        if author_id.startswith('https://openalex.org/'):
            author_id = author_id.split('/')[-1]
        
        url = f"{self.BASE_URL}/authors/{author_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting author by ID: {e}")
            return {}


def print_author_results(results: Dict, title: str):
    """Helper function to print search results in a formatted way."""
    print(f"\n=== {title} ===")
    
    if not results:
        print("No results found or error occurred.")
        return
    
    if 'results' in results:
        authors = results['results']
        meta = results.get('meta', {})
        
        print(f"Found {meta.get('count', 0)} total results (showing {len(authors)})")
        print("-" * 80)
        
        for i, author in enumerate(authors, 1):
            print(f"{i}. {author.get('display_name', 'Unknown')}")
            print(f"   ID: {author.get('id', 'N/A')}")
            print(f"   Works: {author.get('works_count', 0)}")
            print(f"   Citations: {author.get('cited_by_count', 0)}")
            
            # Show affiliations if available
            affiliations = author.get('affiliations', [])
            if affiliations:
                print(f"   Institution: {affiliations[0].get('institution', {}).get('display_name', 'Unknown')}")
            
            # Show ORCID if available
            orcid = author.get('orcid')
            if orcid:
                print(f"   ORCID: {orcid}")
            
            print()


def print_autocomplete_results(results: Dict, title: str):
    """Helper function to print autocomplete results."""
    print(f"\n=== {title} ===")
    
    if not results or 'results' not in results:
        print("No results found or error occurred.")
        return
    
    authors = results['results']
    print(f"Found {len(authors)} autocomplete suggestions")
    print("-" * 80)
    
    for i, author in enumerate(authors, 1):
        print(f"{i}. {author.get('display_name', 'Unknown')}")
        print(f"   Hint: {author.get('hint', 'N/A')}")
        print(f"   Works: {author.get('works_count', 0)}")
        print(f"   Citations: {author.get('cited_by_count', 0)}")
        print()


def search_author_interactive(query: str, searcher: OpenAlexAuthorSearch):
    """Search for a specific author and display results."""
    print(f"OpenAlex Author Search for: '{query}'")
    print("=" * 60)
    
    # Basic search
    print(f"\n🔍 Searching for authors matching '{query}'...")
    search_results = searcher.search_authors(query, per_page=10)
    print_author_results(search_results, f"Search Results for '{query}'")
    
    # Autocomplete search (for shorter queries)
    if len(query.split()) <= 2:  # Only show autocomplete for short queries
        print(f"\n🔍 Autocomplete suggestions for '{query}'...")
        autocomplete_results = searcher.autocomplete_authors(query)
        print_autocomplete_results(autocomplete_results, f"Autocomplete for '{query}'")
    
    # Show detailed info for the first result if available
    if search_results and 'results' in search_results and search_results['results']:
        first_author = search_results['results'][0]
        author_id = first_author['id']
        print(f"\n🔍 Detailed information for top result...")
        author_data = searcher.get_author_by_id(author_id)
        
        if author_data:
            print(f"\n=== Detailed Author Information ===")
            print(f"Name: {author_data.get('display_name', 'Unknown')}")
            print(f"ID: {author_data.get('id', 'N/A')}")
            print(f"Works Count: {author_data.get('works_count', 0)}")
            print(f"Cited By Count: {author_data.get('cited_by_count', 0)}")
            
            # Summary stats
            summary = author_data.get('summary_stats', {})
            print(f"H-index: {summary.get('h_index', 'N/A')}")
            print(f"i10-index: {summary.get('i10_index', 'N/A')}")
            print(f"2-year mean citedness: {summary.get('2yr_mean_citedness', 'N/A')}")
            
            # Current affiliations
            affiliations = author_data.get('affiliations', [])
            if affiliations:
                print(f"\nCurrent Affiliations:")
                for i, aff in enumerate(affiliations[:3], 1):  # Show top 3
                    inst = aff.get('institution', {})
                    print(f"  {i}. {inst.get('display_name', 'Unknown Institution')}")
                    if inst.get('country_code'):
                        print(f"     Country: {inst.get('country_code')}")
            
            # ORCID
            orcid = author_data.get('orcid')
            if orcid:
                print(f"\nORCID: {orcid}")
            
            # Recent works (if available)
            works_api_url = author_data.get('works_api_url')
            if works_api_url:
                print(f"\nWorks API URL: {works_api_url}")


def run_tests(searcher: OpenAlexAuthorSearch):
    """Run the original test suite."""
    print("OpenAlex Author Search Test Script")
    print("=" * 50)
    
    # Test 1: Basic author search
    print("\n🔍 Testing basic author search...")
    search_results = searcher.search_authors("Carl Sagan", per_page=5)
    print_author_results(search_results, "Basic Search Results for 'Carl Sagan'")
    
    # Test 2: Autocomplete search
    print("\n🔍 Testing autocomplete search...")
    autocomplete_results = searcher.autocomplete_authors("ronald sw")
    print_autocomplete_results(autocomplete_results, "Autocomplete Results for 'ronald sw'")
    
    # Test 3: Field-specific search
    print("\n🔍 Testing field-specific search...")
    field_results = searcher.search_authors_by_field("display_name", "john smith", per_page=5)
    print_author_results(field_results, "Field Search Results for 'john smith' in display_name")
    
    # Test 4: Search with diacritics
    print("\n🔍 Testing search with diacritics...")
    diacritic_results = searcher.search_authors("José García", per_page=5)
    print_author_results(diacritic_results, "Search Results for 'José García'")
    
    # Test 5: Get specific author by ID (if we found one)
    if search_results and 'results' in search_results and search_results['results']:
        author_id = search_results['results'][0]['id']
        print(f"\n🔍 Testing get author by ID: {author_id}")
        author_data = searcher.get_author_by_id(author_id)
        if author_data:
            print(f"\nDetailed Author Information:")
            print(f"Name: {author_data.get('display_name', 'Unknown')}")
            print(f"ID: {author_data.get('id', 'N/A')}")
            print(f"Works Count: {author_data.get('works_count', 0)}")
            print(f"Cited By Count: {author_data.get('cited_by_count', 0)}")
            print(f"H-index: {author_data.get('summary_stats', {}).get('h_index', 'N/A')}")
            print(f"i10-index: {author_data.get('summary_stats', {}).get('i10_index', 'N/A')}")
    
    print("\n✅ All tests completed!")
    print("\nFor more information, visit: https://docs.openalex.org/api-entities/authors/search-authors")


def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(
        description='Search for authors using the OpenAlex API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3.11 openalex_author_search.py "Carl Sagan"
  python3.11 openalex_author_search.py "Marie Curie"
  python3.11 openalex_author_search.py "John Smith"
  python3.11 openalex_author_search.py --test  # Run test suite
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Author name to search for'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run the test suite with predefined examples'
    )
    
    args = parser.parse_args()
    
    # Initialize the search client
    searcher = OpenAlexAuthorSearch()
    
    if args.test:
        # Run the original test suite
        run_tests(searcher)
    elif args.query:
        # Search for the specified author
        search_author_interactive(args.query, searcher)
    else:
        # No arguments provided, show help
        parser.print_help()
        print("\nYou can also run the test suite with: --test")
        return
    
    print(f"\n📚 For more information, visit: https://docs.openalex.org/api-entities/authors/search-authors")


if __name__ == "__main__":
    main()



