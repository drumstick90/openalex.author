# OpenAlex Author Search Test Script

This repository contains a Python script to test the OpenAlex API for searching authors. The script demonstrates various ways to search for authors using the OpenAlex API.

## OpenAlex API Documentation

The OpenAlex API is a comprehensive database of scholarly works and authors. The author search functionality allows you to:

- **Basic Search**: Search authors by name using the `search` parameter
- **Autocomplete**: Fast type-ahead search for creating responsive UIs
- **Field-specific Search**: Search within specific fields like `display_name`
- **Get by ID**: Retrieve detailed information about a specific author

### API Endpoints

- **Author Search**: `https://api.openalex.org/authors?search={query}`
- **Autocomplete**: `https://api.openalex.org/autocomplete/authors?q={query}`
- **Field Search**: `https://api.openalex.org/authors?filter=display_name.search:{query}`
- **Get Author**: `https://api.openalex.org/authors/{author_id}`

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script with an author name:
```bash
python3.11 openalex_author_search.py "Carl Sagan"
```

Or run the test suite:
```bash
python3.11 openalex_author_search.py --test
```

## Usage Examples

### Command Line Usage
```bash
# Search for a specific author
python3.11 openalex_author_search.py "Marie Curie"
python3.11 openalex_author_search.py "Albert Einstein"
python3.11 openalex_author_search.py "Jane Smith"

# Run the test suite
python3.11 openalex_author_search.py --test

# Show help
python3.11 openalex_author_search.py --help
```

### Programmatic Usage
```python
from openalex_author_search import OpenAlexAuthorSearch

searcher = OpenAlexAuthorSearch()
results = searcher.search_authors("Carl Sagan")
```

### Autocomplete Search
```python
autocomplete_results = searcher.autocomplete_authors("ronald sw")
```

### Field-specific Search
```python
field_results = searcher.search_authors_by_field("display_name", "john smith")
```

## Features

- ✅ Basic author search with flexible name matching
- ✅ Autocomplete functionality for type-ahead search
- ✅ Field-specific search capabilities
- ✅ Author retrieval by OpenAlex ID
- ✅ Handles diacritics and variations in names
- ✅ Comprehensive error handling
- ✅ Formatted output for easy reading

## API Features

- **Flexible Name Matching**: Searches without middle initials return names with and without middle initials
- **Diacritic Support**: Searches handle accented characters flexibly
- **No Rate Limiting**: Free access with no API key required
- **Rich Metadata**: Returns work counts, citation counts, affiliations, and more

## Example Output

The script will show results like:
```
=== Basic Search Results for 'Carl Sagan' ===
Found 2 total results (showing 2)
--------------------------------------------------------------------------------
1. Carl Sagan
   ID: https://openalex.org/A41008148
   Works: 284
   Citations: 9876
   Institution: Cornell University
   ORCID: https://orcid.org/0000-0002-9366-2671
```

## Links

- [OpenAlex API Documentation](https://docs.openalex.org/api-entities/authors/search-authors)
- [OpenAlex Website](https://openalex.org)
- [Author Search Documentation](https://docs.openalex.org/api-entities/authors/search-authors)
