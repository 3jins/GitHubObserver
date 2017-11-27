import requests
from bs4 import BeautifulSoup

# Get inputs that have a specific name.
def get_specific_name_input(inputs, names):
    specific_inputs = []
    for input in inputs:
        if input['name'] in names:
            specific_inputs.append(input)
            # if input['name'] in tokens:
            #     tokens[input['name']].append(input['data-autocheck-authenticity-token'])
            # else:
            #     tokens[input['name']] = [input['data-autocheck-authenticity-token']]
    return specific_inputs


# Get tokens in GitHub login page
def get_login_token():
    tokens = {}
    url = 'https://github.com/login'
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text, "html.parser")
    # soup = BeautifulSoup(source_code, "html.parser")

    inputs = soup.find_all('input')
    inputs = get_specific_name_input(inputs, ['authenticity_token'])

    for input in inputs:
        if input['name'] in tokens:
            tokens[input['name']].append(input['value'])
        else:
            tokens[input['name']] = [input['value']]

    return tokens


def crawl():
    tokens = get_login_token()
    print(tokens)

    # news_feed = soup.find_all(class_='news')
    # print(news_feed)

