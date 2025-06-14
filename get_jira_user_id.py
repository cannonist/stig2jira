import os
import sys
import requests

# .env
from dotenv import load_dotenv
load_dotenv()

# Usage: python get_jira_user_id.py <user_email>
def get_jira_user_id(email):
    jira_url = os.getenv("JIRA_URL")
    jira_user = os.getenv("JIRA_USER")
    jira_token = os.getenv("JIRA_TOKEN")

    if not all([jira_url, jira_user, jira_token]):
        print("ERROR: Missing Jira credentials in .env")
        sys.exit(1)

    response = requests.get(
        f"{jira_url}/rest/api/3/user/search?query={email}",
        auth=(jira_user, jira_token),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        print(f"ERROR: {response.status_code} - {response.text}")
        sys.exit(1)

    users = response.json()
    if not users:
        print(f"No user found for email: {email}")
        return

    for user in users:
        print(f"\nAccount ID: {user['accountId']}")
        print(f"Name: {user.get('displayName')}")
        print(f"Email: {user.get('emailAddress', '[hidden]')}")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_jira_user_id.py <email>")
        sys.exit(1)

    get_jira_user_id(sys.argv[1])