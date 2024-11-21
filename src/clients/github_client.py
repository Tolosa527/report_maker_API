import requests
from datetime import datetime, timedelta
from src.settings import settings
from src.logger import Logger

log = Logger().get_logger(__name__)

GITHUB_HEADERS = settings.get_github_headers


def get_github_data(username, start_date, end_date):
    start_date = f'{start_date}T00:00:00Z'
    end_date = f'{end_date}T23:59:59Z'
    url = f'https://api.github.com/search/issues?q=author:{username}+type:pr+created:{start_date}..{end_date}'
    response = requests.get(url, headers=GITHUB_HEADERS)
    log.debug(f"Github response: {response.json()}")
    return response.json()


def get_paticipation_data(username, start_date, end_date):
    start_date = f'{start_date}T00:00:00Z'
    end_date = f'{end_date}T23:59:59Z'
    url = f'https://api.github.com/search/issues?q=commenter:{username}+type:pr+created:{start_date}..{end_date}'
    response = requests.get(url, headers=GITHUB_HEADERS)
    log.debug(f"Github response: {response.json()}")
    return response.json()


if __name__ == '__main__':
    today = datetime.today().strftime('%Y-%m-%d')
    username = 'Tolosa527'
    own_data = get_github_data(
        username=username, start_date=today - timedelta(days=7), end_date=today
    )
    participant_data = get_paticipation_data(
        username=username, start_date=today, end_date=today
    )
    items = own_data['items']
    for item in items:
        title = item.get('title')
        pull_request_url = item.get('pull_request').get('url')
        print("Own Pull Request")
        print("-----------------")
        print(f'Title: {title}')
        print(f'URL: {pull_request_url}\n')

    items = participant_data['items']
    for item in items:
        title = item.get('title')
        pull_request_url = item.get('pull_request').get('url')
        print("Code Review")
        print("------------")
        print(f'Title: {title}')
        print(f'URL: {pull_request_url}\n')
