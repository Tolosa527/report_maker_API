from openai import OpenAI
from src.settings import settings
from logging import getLogger

log = getLogger(__name__)

client = OpenAI(api_key=settings.get_open_ai_api_key)


def generate_report_text(data: dict) -> str | None:
    prompt = f"""
    The data ordered by date is: {data}
    The schema of the data is:
    {{
        "Date": {{
            "github": [],
            "jira": [],
            "tasks": []
        }}
    }}

    Based on the data provided, generate a detailed report for the last sprint.
    The report should include the following information:

    Use Date as the key to organize the information.
    - Jira issues
    - GitHub issues
    - Tasks

    * If GitHub's data has the role "participant", the line should include the prefix [CODE REVIEW] else the line should not include the prefix.
    Example of output: [CODE REVIEW] - text - 📝

    * Include the status of each task using emojis:
        ✅ for completed (closed/finalized),
        🚧 for in progress (open/en curso/QA Staging),
        🛑 for stopped tasks/issues.
        📝 code reviews
        📊 reports and research
        📞 calls and meetings
"""
    # Send the prompt to ChatGPT API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a project manager for a software development team. You need to generate a detailed report for the last sprint."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": "Give to the report a format to be shared on a slack channel."},
            ],
            max_tokens=1024,  # Adjust the max tokens depending on the size of your report
            temperature=0.3,
        )

        # Extract the report from the response
        report = response.choices[0].message.content
        return report
    except Exception as e:
        return f"An error occurred: {str(e)}"
