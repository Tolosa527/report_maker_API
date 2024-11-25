import requests
from datetime import datetime
from src.settings import settings
from src.logger import Logger

log = Logger().get_logger(__name__)

GITHUB_HEADERS = settings.get_github_headers


def get_github_data(
    username: str,
    start_date: datetime,
    end_date: datetime
) -> dict:
    query = get_query(
        start_date=start_date,
        end_date=end_date,
        author=username
    )
    response = make_request(query)
    if not response.ok:
        log.error(f"Error fetching Github data: {response.text}")
        return {}
    return response.json()


def get_paticipation_data(username, start_date, end_date):
    query = get_query(
        start_date=start_date,
        end_date=end_date,
        commenter=username
    )
    response = make_request(query)
    if not response.ok:
        log.error(f"Error fetching Github participation data: {response.text}")
        return {}
    return response.json()


def make_request(url: str) -> requests.Response:
    try:
        response = requests.get(url, headers=GITHUB_HEADERS)
        log.debug(f"Github response: {response.json()}")
    except Exception as e:
        log.error(f"Error making request to {url}: {str(e)}")
        return {}
    return response


def get_query(
    start_date: datetime,
    end_date: datetime,
    author: str | None = None,
    commenter: str | None = None,
) -> str:
    search_issues_url = "https://api.github.com/search/issues"
    base_q = "?q=is:pr+org:invibeme+updated:"
    query = search_issues_url + base_q + "{}..{}".format(
        start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    if author:
        query += f"+author:{author}"
    if commenter:
        query += f"+commenter:{commenter}"

    return query
