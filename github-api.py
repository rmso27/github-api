"""
Script to query GitHub API and get yearly contributions
"""

## IMPORTS ##

# Import modules
import requests
import json
from datetime import date
import configparser

## MAIN VARS ##

# Setup configuration file
config = configparser.ConfigParser()
config.read('configs/configs.ini')

# Read configuration file
api_url = config['github']['API_URL']
graph_api_url = config['github']['GRAPH_API_URL']
auth_token = config['github']['AUTH_TOKEN']

# Request parameters
header = {'Accept': 'application/vnd.github.v3+json', 'Authorization': auth_token}

## FUNCTIONS ##

# Get GitHub user details (creation date)
def get_user_details(api_url):

    response = requests.get(api_url)
    data = response.json()
    created_at = data['created_at']

    return created_at

# Get GitHub yearly contributions
def get_contributions(created_at, graph_api_url, header):

    current_year = date.today().year
    contribution_year =  int(created_at[0:4])
    contributions = []

    """
    Query the API through for yearly contributions
    (from year when the account was created till current year)
    """
    while contribution_year <= current_year:
        variables = {'username': 'rmso27', 'fromDate': str(contribution_year) + '-01-01T00:01:00Z'  , 'toDate': str(contribution_year) + '-12-31T23:59:59Z'}
        query = """
            query($username: String!, $fromDate: DateTime!, $toDate: DateTime!) {
                user(login: $username){
                    contributionsCollection (from: $fromDate, to: $toDate) {
                        contributionCalendar {
                            totalContributions
                        }
                    }
                }
            }
        """

        # POST request
        response = requests.post(graph_api_url, json = {'query': query, 'variables': variables}, headers = header)
        print(response)
        data = response.json()

        # Build list of contributions
        contributions += [{'year': contribution_year, 'contributions': data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']}]

        contribution_year +=1

    return contributions

## MAIN ##

created_at = get_user_details(api_url)
contributions = get_contributions(created_at, graph_api_url, header)

# Write results into a JSON file
with open('yearly_contributions.json', 'w') as results:
    results.write(json.dumps(contributions))