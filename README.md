# Google-Sheets-To-Slack
Turn google form submissions into slack notifications

## Setup
* Create Google Cloud project w/ Google Drive, Google Drive Acitvity, and Google Sheets API's enable.d
* Create a service account in that project and download the credentials JSON and name it `creds.json`
* Copy `ex-config.toml` to `config.toml` and fill out with a list of Google Sheet URL's and the Slack webhook URL
* `make setup` to install required pip packages
* `make run` to run the monitor (probably put in a cronjob?)
* Profit??
