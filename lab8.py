# Cat facts
import requests
import pandas as pd

# Extract cat facts and save them to a CSV file
def extract_cat_facts():
    url = 'https://cat-fact.herokuapp.com/facts'

    response = requests.get(url)

    # Check whether the request contains errors
    # Status code 200 (Success/OK)
    if response.status_code == 200:
        data = response.json()

        # Check if the response is a list of facts
        if isinstance(data, list):
            # Convert the list of facts to a DataFrame
            df = pd.DataFrame(data)

            # Save DataFrame to CSV
            df.to_csv('cat_facts.csv', index=False)
            print('Cat facts saved to cat_facts.csv')
        else:
            print('Error: The response is not a list of facts.')
            print(data)
    else:
        print(f'Error: Request failed. Status Code: {response.status_code}')


# Anime list
import json
import requests
import secrets

CLIENT_ID = 'a9c76247347a5fbd7d6ebcf47f6f8489'
# CLIENT_SECRET = 'YOUR CLIENT SECRET'


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID#, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        # 'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent=4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}'
    })

    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")


def authorisation():
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge)

    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    token = generate_new_token(authorisation_code, code_verifier)

    print_user_info(token['access_token'])


def displayMenu():
    print("Select which dataset you want to access: \n1. Cat Facts (does not require authentication)\n2. Anime List (requires authentication)")
    i = int(input())
    if i==1:
        extract_cat_facts()
    elif i == 2:
        authorisation()
    else:
        print("Invalid choice. Re-enter:\nSelect which dataset you want to access.:  \n1.Cat Facts (does not require authentication)\n2.Anime List (requires authentication)")
        i = int(input())

displayMenu()

