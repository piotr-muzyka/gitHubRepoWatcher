import json
import logging
import os
import sys
import time

import requests
from redis import Redis

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
redis = Redis(host='redis-headless', port=6379)


class Settings:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USER = os.getenv('GITHUB_USER')
    BASE_URL = f'https://api.github.com/users/{GITHUB_USER}/repos'
    HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}


def get_api_repositories(base_url, headers):
    response = requests.get(base_url, headers=headers)
    logging.info(f'Status code: {response.status_code}')
    return response.json()


def list_repositories(git_api_response):
    repositories = [repository.get('id') for repository in git_api_response]
    logging.info(f'Repos from API call: {repositories}')
    return repositories


def get_db_repositories():
    if redis.get('repositories'):
        repositories = json.loads(redis.get('repositories').decode('utf-8'))
        logging.info(f'Repos from DB call: {repositories}')
        return repositories
    return []


def check_for_new_repositories(api_repositories, db_repositories):
    diff = set(api_repositories) - set(db_repositories)
    if diff:
        logging.info(f'New repository detected with ID: {diff}')
        _update_repositories_state(api_repositories)
        # post_message_to_slack(f'New repository detected with ID: {diff}')
        return True
    logging.info('No new repos since last check.')
    return False


def _update_repositories_state(api_repositories):
    redis.set('repositories', json.dumps(api_repositories))
    return


if __name__ == '__main__':
    while True:
        api_response = get_api_repositories(Settings.BASE_URL, Settings.HEADERS)
        repositoriesAPI = list_repositories(api_response)
        repositoriesDB = get_db_repositories()
        check_for_new_repositories(repositoriesAPI, repositoriesDB)
        time.sleep(20)