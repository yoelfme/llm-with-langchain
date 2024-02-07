# from langchain_community.utilities import SerpAPIWrapper
from langchain.serpapi import SerpAPIWrapper

def get_profile_url(text: str) -> str:
    """Searches for LinkedIn profile page"""
    search = SerpAPIWrapper()

    results =  search.run(f'{text}')

    return results
