# STIG2Jira

**STIG2Jira** is a Python tool that parses `.cklb` checklist files from DISA STIG compliance checks and generates structured Jira tickets using the Jira REST API.

It helps automate some of my security compliance workflows by turning open findings into trackable tasks — formatted using Atlassian Document Format (ADF).

## Features

- Parses `.cklb` JSON files directly
- Filters `open` STIG findings
- Creates clean, formatted Jira tickets with:
  - Bolded metadata
  - Blockquoted fix & check guidance
- Dry-run mode with Markdown preview
- Uses `.env` config for Jira API credentials

![Image](https://github.com/user-attachments/assets/22b1816f-69de-4162-8321-e95cf9f519d0)

## Requirements

- Python 3.8+
- A test or production Jira Cloud environment
- Jira project and user API access

Install dependencies:

```bash
pip install -r requirements.txt
```
--- 

## Usage

python stig2jira.py path/to/checklist.cklb

Options:
Flag	    Description
--confirm	Push tickets to Jira
(no flag)	Generate tickets_draft.md preview

Example

python stig2jira.py ./RHEL8.cklb
 -> Generates tickets_draft.md

python stig2jira.py ./RHEL8.cklb --confirm
 -> Pushes tickets to Jira

## Environment Setup

Create a .env file in the project root with:

JIRA_URL=https://yourdomain.atlassian.net
JIRA_USER=your-email@example.com
JIRA_API_KEY=your-api-token
JIRA_PROJECT_KEY=SEC
JIRA_REPORTER_ID=123456

## Project Structure

```
stig2jira/
├── stig2jira.py         # Main CLI runner
├── adf_formatter.py     # ADF description generator
├── .env                 # Config and API credentials
└── tickets_draft.md     # Preview file (optional)
```
## Roadmap / Todo

- [ ] Better formatting in draft_tickets.md
- [ ] Better formatting of resulting Jira tickets
    - I'd like them to be cleaner and more actionable for assignees
