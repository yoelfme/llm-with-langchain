import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str):
    """Scrape information from LinkedIn profile
    Manually scrape the information from LinkedIn profile
    """
    api_endpoint = os.environ.get("LINKEDIN_SCRAPER_ENDPOINT")

    if api_endpoint is None:
        raise Exception("LINKEDIN_SCRAPER_ENDPOINT is not set")

    response = requests.get(api_endpoint)

    if response.status_code != 200:
        raise Exception("LinkedIn scraper is not running")

    return clean_linkedin_data(response.json())


def clean_linkedin_data(linkedin_data: dict):
    """Clean LinkedIn data
    Clean the data from LinkedIn profile
    """
    data = {
        k: v
        for k, v in linkedin_data.items()
        if v not in [[], "", None]
            and k not in ['profile_also_viewd', 'certifications']
    }

    if data.get('groups'):
        for group in data['groups']:
            group.pop('profile_pic_url')

    return data