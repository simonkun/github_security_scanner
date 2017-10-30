# Main file - where the magic happens
# Check out the README file if you need some help
# Written by Simon Theodore Kun

import sys
import argparse
import getpass
import logging
import os
import requests
import json

def quarantine(organisation, bad_user):
    '''
    This function is get all the teams a user is part of and remove them and then add them to the 'Qurantine' team.

    Arguments:
    organisation -- the name of the GitHub organisation to scan
    bad_user -- the username of the user that is to be quarantined
    '''
    # get a list of all the different teams for specified organisation
    req_teams = requests.get('https://api.github.com/orgs/'+ organisation + '/teams', auth=(user, password))

    # loop and get each teams id and name
    for record in req_teams.json():
        target_id = record['id']
        target_name = record['name']
        # check is user is in the team
        req_ismember = requests.get('https://api.github.com/teams/' + str(target_id) + '/memberships/' + bad_user + '', auth=(user, password))
        logging.debug(req_ismember.status_code)
        # if user is in team then remove
        if req_ismember.status_code == 200: #200 means yes
            logging.info(bad_user + ' is a member of ' + target_name + ' team')
            req_delete = requests.delete('https://api.github.com/teams/' + str(target_id) + '/members/' + bad_user, auth=(user, password))
            if req_delete.status_code == 204: #204 means yes
                logging.info(bad_user + ' Successfully removed from ' + target_name)
            else:
                logging.error('Failed to remove user')
        elif req_ismember.status_code == 404:
            logging.warning(bad_user + ' is not a member of the ' + target_name +
            ' team')
        else:
            logging.error('request for team membershps failed')

    # finally add the user to the quaratine team
    req_quaratine = requests.put('https://api.github.com/teams/' + str(target_id) + '/members/' + bad_user, auth=(user, password))
    if req_quaratine.status_code == 204: #204 means yes
        logging.info(bad_user + ' added to quarantine')
    else:
        logging.error(bad_user + ' failed to add to qurantine')
    return;

# check is users have 2FA configured. if they don't then banish them to the
# quarantine team (where they cannot do damage)
def two_factor(organisation):
    '''
    This function is checking is users have 2FA enabled and then quaratining the ones that do not.

    Arguments:
    organisation -- the name of the GitHub organisation to scan
    '''
    # get list of bad users and then quarantine them
    #payload = {'filter': '2fa_disabled'}
    r = requests.get('https://api.github.com/orgs/'+ organisation + '/members', auth=(user, password), params={'filter' : '2fa_disabled'})

    # If we get a good response (Http 200) then we can do stuff
    if r.status_code == 200: #200 means yes
        for record in r.json():
            target_name = record['login']
            logging.info(target_name + ' does not have 2FA enabled')
            quarantine(organisation, target_name)
    else:
        logging.error('failed to get list of users not using 2FA')
    return;

def bad_commits(organisation):
    '''
    This function is checking all commits across all respositories for a given organisation and for anyone that has bad commit signatures - they go to quarantine

    Arguments:
    organisation -- the name of the GitHub organisation to scan
    '''
    #get repos for orgs
    req_ismember = requests.get('https://api.github.com/orgs/' + organisation + '/repos', auth=(user, password))
    for repo in req_ismember.json():
        repo_name = repo['name']
        req_commits = requests.get('https://api.github.com/repos/' + organisation + '/' + repo_name + '/commits', auth=(user, password))

        for commit in req_commits.json():
            commit_author = commit['author'] #who did the commit
            commit_username = commit_author['login'] #username if need to quarantine
            commit_details = commit['commit'] #details on commit
            commit_verification = commit_details['verification'] #verification details
            commit_verified = commit_verification['verified'] #boolean result

            if commit_verified == False:
                logging.info(commit_username + ' has some bad commits and will be quarantined')
                quarantine(organisation, str(commit_username))
    return;

# Main Body of Code
#
# Parser for user to specify what actions they want to perform
# will be more useful as plugins increase
# TODO include options for just specific activites especially logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description='Use this application to scan a Github organisation for security issues')
# need to know who we are scanning
parser.add_argument('organisation', help='specify the name of the github organisation you would like to scan')

# parse the args
args = parser.parse_args()

# this is out target
target_org = args.organisation

# get creds for authentication into Github
user = getpass.getpass("Username:")
password = getpass.getpass("Password:")

# it begins
logging.info('Beginning Secuirty Scan on ' + target_org)

# look and tell me about who does not have 2FA enabled
two_factor(target_org)

# now find if there are any bad commits
bad_commits(target_org)

logging.info('Scan Complete on ' + target_org)
