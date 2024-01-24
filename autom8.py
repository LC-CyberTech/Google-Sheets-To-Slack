import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
import json
import toml
from datetime import datetime

if not os.path.exists("config.toml"):
    print("Please create a config.toml file")
    exit(1)

config = toml.load("config.toml")

# Set up Slack webhook URL
SLACK_WEBHOOK_URL = config['slack_url']

SHEET_URLS = config['sheet_urls']

if not os.path.exists("creds.json"):
    print("Please download your Google Sheets API credentials and save them as creds.json")
    exit(1)

# Set up credentials for accessing Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

def get_last_modified_time(sheet):
    # Get the last modified time of the sheet
    properties = sheet.get_properties()
    return datetime.strptime(properties['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")

def send_to_slack(form_url):
    # Your function to send data to Slack
    payload = {'text': f"Google Sheet updated: {form_url}"}
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))

def main():
    # List of Google Sheets URLs
    sheet_urls = SHEET_URLS

    if not os.path.exists(".data"):
        os.makedirs(".data")

    # Check each sheet for updates
    for sheet_url in sheet_urls:
        sheet = client.open_by_url(sheet_url)

        # Get the last modified time of the sheet
        last_modified_time = get_last_modified_time(sheet)

        # Check if the sheet has been modified since the last run
        if os.path.exists(f".data/{sheet.title}_last_modified.txt"):
            with open(f".data/{sheet.title}_last_modified.txt", "r") as file:
                previous_modified_time = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S.%f")
                if last_modified_time > previous_modified_time:
                    send_to_slack(sheet_url)
        else:
            # First run, store the current modified time
            with open(f".data/{sheet.title}_last_modified.txt", "w") as file:
                file.write(last_modified_time.strftime("%Y-%m-%d %H:%M:%S.%f"))

if __name__ == "__main__":
    main()
