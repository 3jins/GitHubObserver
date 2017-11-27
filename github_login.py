from bs4 import BeautifulSoup


# Get inputs that have a specific name.
def get_specific_name_input(inputs, names):
    specific_inputs = []
    for input in inputs:
        if input['name'] in names:
            specific_inputs.append(input)
    return specific_inputs


# Get tokens in GitHub login page
def get_login_token(session):
    tokens = {}
    url = 'https://github.com/login'
    source_code = session.get(url)
    soup = BeautifulSoup(source_code.text, "html.parser")

    inputs = soup.find_all('input')
    inputs = get_specific_name_input(inputs, ['authenticity_token'])

    for input in inputs:
        tokens[input['name']] = input['value']

    return tokens


# Sign in with given accoutn information
def signin(session, id, pw):
    token = get_login_token(session)
    login_info = {
        'login': id,
        'password': pw,
    }
    login_info.update(token)

    login_response = session.post('https://github.com/session', data=login_info)
    if login_response.status_code == 200:
        print("Login Success")
    else:
        print(str(login_response.status_code) + ": " + str(login_response.reason))