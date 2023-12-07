#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Run script from command line via python3 find_pats.py

import click
import datetime
import time

from github import Github
from github.GithubException import RateLimitExceededException
from tqdm import tqdm


def search_github(auth: Github):
    """Search the GitHub API for repositories with exposed PATs.
    Args:
        auth: A Github authenticate object.
    Returns:
        A nested list of GitHub repositories returned with exposed PATs. Each result list contains the repository name,
        url, and description.
    """

    # set-up query
    query = r'^github_pat_[A-Za-z0-9_]+$'
    results = auth.search_code(query)

    # print results
    print(f'Found {results.totalCount} repo(s)')

    for result in tqdm(results, total=results.totalCount, desc='Processing Results'):
        try:
            # Access result attributes as needed
            repo_name = result.repository.full_name
            file_path = result.path

            # Print or process the information
            print(f"Repository: {repo_name}, File: {file_path}")

            time.sleep(2)
        except RateLimitExceededException:
            time.sleep(60)
            print("Rate limit exceeded, waiting for 60 seconds...")


@click.command()
@click.option('--token', prompt='Please enter your GitHub Access Token')
def main(token: str) -> None:

    # initialize and authenticate GitHub API
    auth = Github(token)

    # search repositories on GitHub
    search_github(auth)


if __name__ == '__main__':
    main()
