# github-api

## Description
Script to query GitHub API and get yearly contributions

## Setup & Execution
1. Edit the configs/configs.ini file and update the following the vars API_URL and AUTH_TOKEN
2. Execute the script
python github-api.py

## Sample of the output
The results are written on afile called yearly_contributions.json

{
    "year": 2022,
    "contributions": 132
}