import requests
import json
from src.settings import settings
from datetime import datetime, timedelta

MESSAGE = 'Hello, Slack!'
SLACK_TOKEN = settings.get_slack_token
CHANNEL_ID = settings.get_slack_channel_id


def send_slack_message(text):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }
    data = {
        'channel': CHANNEL_ID,
        'text': text
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200 and response.json().get('ok'):
        return 'Message sent successfully'
    else:
        return f'Failed to send message {response.text}'


def generate_message(
    start_date: datetime,
    end_date: datetime,
    jira_data: dict,
    github_data: dict
) -> str:
    """
    Generates the message to be sent to Slack.

    Args:
        start_date: Start date of the report
        end_date: End date of the report
        jira_data: Data from Jira API
        github_data: Data from Github API

    Returns:
        str: Message to be sent to Slack
    """
    # Initialize the message
    message = ''

    while start_date < end_date:
        message += f'{start_date.strftime("%A")} \n'

        # Add the Github data to the message
        message += '\n'

        for item in github_data['items']:
            item_date = datetime.strptime(
                item['created_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S%z'
            )
            if item_date.date() == start_date.date():
                message += f'Title: {item["title"]}\n'
                message += f'URL: {item["html_url"]}\n'
                message += '\n'

        # Add the Jira data to the message
        message += '\n'
        for issue in jira_data['issues']:
            item_date_str = issue['fields']['updated'][:-3].split('.')[0]
            item_date = datetime.strptime(
                item_date_str, '%Y-%m-%dT%H:%M:%S'
            )
            status = issue["fields"]["status"]["name"]
            if (
                item_date.date() == start_date.date()
                and status in ["Finalizada", "Control de calidad"]
            ):
                message += f'Summary: {issue["fields"]["summary"]}\n'
                message += f'Status: {status}\n'
                message += f'Updated at: {issue["fields"]["updated"]}\n'
                message += f'Key: {issue["key"]}\n'
                message += '\n'

        # Add a newline at the end of the message
        message += '\n'

        start_date += timedelta(days=1)

    return message


if __name__ == '__main__':
    send_slack_message(SLACK_TOKEN, CHANNEL_ID, MESSAGE)
