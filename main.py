import requests
import getpass

import github_bot
import facebook_bot


if __name__ == '__main__':
    with requests.session() as session:
        github_login = github_bot.GitHubLogin(session, id=input('id: '), pw=getpass.getpass('password: '))
        github_login.login()
        fb_bot = facebook_bot.FacebookBot()
        fb_bot.login()
        github_observe = github_bot.GitHubObserve(session, fb_bot)
        print("\nPut 'quit' to quit the loop.\n")

        github_observe.get_new(30)
