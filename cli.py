import argparse
from datetime import datetime, timedelta
from src.socket_client import SocketClient


def create_message(message: str) -> None:
    socket_client = SocketClient()
    socket_client.send_message(message=message)
    socket_client_response = socket_client.get_response()
    socket_client.close_connection()
    if socket_client_response:
        print(socket_client_response)
    else:
        print('No response from server')
    exit()


if __name__ == '__main__':

    """
    Weekly report maker
    Usage:
        python main.py [--start_date=<start_date>] [--end_date=<end_date>] [--add_task=<task>] [--get_tasks] [--get_report] [--send_report]
    Options:
        --start_date=<start_date>   Start date in YYYY-MM-DD format
        --end_date=<end_date>       End date in YYYY-MM-DD format
        --add_task=<task>           Add task to the database
        --get_tasks                 Get tasks from the database
        --get_report                Get report for the week
        --send_report               Send report to the slack channel
    Description:
        This script is used to generate weekly reports. It provides various options to interact with the report generation process.
        Options:
            --start_date=<start_date>
                Specifies the start date for the report. If not provided, it defaults to the current date minus 6 days.
            --end_date=<end_date>
                Specifies the end date for the report. If not provided, it defaults to the current date.
            --add_task=<task>
                Adds a task to the database. The task should be provided as a string.
            --get_tasks
                Retrieves tasks from the database within the specified date range.
            --get_report
                Retrieves the report for the week. If start date is not provided, it defaults to the previous week.
            --send_report
                Sends the report to the slack channel.
    Examples:
        1. Generate report for the current week:
            python main.py --get_report
        2. Add a task to the database:
            python main.py --add_task="Fix bug in login module"
        3. Get tasks for a specific date range:
            python main.py --get_tasks --start_date=2022-01-01 --end_date=2022-01-07
        4. Send the report to the slack channel:
            python main.py --send_report
    """

    parser = argparse.ArgumentParser(description='Weekly report maker')
    parser.add_argument('--start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end_date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--add_task', type=str, help='Add task to the database')
    parser.add_argument('--get_tasks', action='store_true', help='Get tasks from the database')
    parser.add_argument('--get_report', action='store_true', help='Get report for the week')
    parser.add_argument('--send_report', action='store_true', help='Send report to the slack channel')

    args = parser.parse_args()

    start_date = args.start_date
    end_date = args.end_date
    add_task = args.add_task
    get_tasks = args.get_tasks
    get_report = args.get_report
    send_report = args.send_report

    if not start_date and not end_date:
        start_date = (
            datetime.today() - timedelta(days=7)
        ).strftime('%Y-%m-%d')
        end_date = datetime.today().strftime('%Y-%m-%d')

    if not start_date:
        start_date = datetime.today().strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')

    if add_task:
        create_message(f"add_task: {add_task}")

    if get_tasks and start_date and end_date:
        create_message(f"get_tasks: {start_date} 00:00:00 - {end_date} 23:59:59")

    if send_report:
        create_message(f"send_slack_report: {start_date} - {end_date}")

    if get_report:
        create_message(f"get_report: {start_date} - {end_date}")
