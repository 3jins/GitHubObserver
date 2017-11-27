import requests
import getpass

import github_login
import github_crawl


if __name__ == '__main__':
    with requests.session() as session:
        github_login.signin(session, id=input('id: '), pw=getpass.getpass('password: '))