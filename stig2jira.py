import sys
import os
import json
import argparse
import requests

# .env 
from dotenv import load_dotenv
load_dotenv()

# markdown to adf
from adf_formatter import stig_check_to_adf

jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_token = os.getenv("JIRA_TOKEN")
jira_project_key = os.getenv("JIRA_PROJECT_KEY")
jira_issue_type = os.getenv("JIRA_ISSUE_TYPE")
jira_reporter_id = os.getenv("JIRA_REPORTER_ID")


def parse_cklb(file_path):
    with open(file_path, "r", encoding="utf-8") as checklist:
        data = json.load(checklist)
    
    tickets = []
    stigs = data.get("stigs", [])

    for stig in stigs:

        stig_name = stig.get("display_name") # Alternatively "stig_name" :: name of the file 

        for rule in stig.get("rules",[]):

            if rule.get("status") != "open":
                continue

            ticket = {
                "summary": f"{rule.get('group_id')} - {rule.get('rule_title')}",
                "stig_name": stig_name,
                "group_id": rule.get("group_id"),
                "severity": rule.get("severity"),
                "status": rule.get("status"),
                "fix_text": rule.get("fix_text", ""),
                "check_content": rule.get("check_content", ""),
                "finding_details": rule.get("finding_details", "")
            }

            tickets.append(ticket)
    
    return tickets


def write_markdown(tickets, source_filename):
    
    with open("draft_tickets.md", "w", encoding="utf-8") as file:
        file.write(f"# Draft Jira Tickets from {os.path.basename(source_filename)}\n\n")

        for ticket in tickets:
            file.write(json.dumps(ticket, indent=))
            file.write("\n" + "-"*80 + "\n\n")


def create_jira_ticket(ticket):

    if not all([jira_url, jira_user, jira_token, jira_project_key, jira_issue_type]): 
        print("ERROR: Jira credentials not fully set in .env")
        return
    
    auth = (jira_user, jira_token)

    fields = {
        "project": {"key": jira_project_key},
        "summary": ticket["summary"],
        "description": stig_check_to_adf(ticket),
        "issuetype": {"name": ticket.get("issue_type", "Task")}
    }
    
    if jira_reporter_id:
        fields["reporter"] = {"id": jira_reporter_id}
    
    payload = {"fields": fields}

    # Request
    response = requests.post(
        f"{jira_url}/rest/api/3/issue",
        headers={"Content-Type": "application/json"},
        # data=payload,
        json=payload,
        auth=(jira_user, jira_token)
    )

    # Response
    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"Created Jira ticket: {issue_key}")
        return issue_key
    else:
        print(f"Failed to create ticket: {response.status_code}")
        print(f"    -> {response.text}")
        return None
    

def main():

    parser = argparse.ArgumentParser(description="Generate Jira tickets from a STIG checklist (.cklb) file")
    parser.add_argument("file", help="Path to the .cklb file")
    parser.add_argument("--confirm", action="store_true", help="Send draft tickets to Jira")
    
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    tickets = parse_cklb(args.file)

    for i, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            print(f"ERROR: Ticket {i} is a {type(ticket)}: {ticket}")
            continue

    if not args.confirm:
        write_markdown(tickets, args.file)
        print(f"\nDraft saved to 'tickets_draft.md'")
        print(f"Run with --confirm to push tickets to Jira.\n")
        return

    for ticket in tickets:
        create_jira_ticket(ticket)

if __name__ == "__main__":    
    main()

