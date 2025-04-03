import pandas as pd
import requests

api_base = 'https://api.github.com'
owner = 'amzn'
url_followers = f'{api_base}/users/{owner}/followers'
token = 'meu_token'
headers = {'Authorization': f'Bearer {token}',
           'X-GitHub-Api-Version': '2022-11-28'}
followers_list = []
contador = 1
while True:
    url = f'{url_followers}?page={contador}'
    r = requests.get(url=url, headers=headers)
    json_page = r.json()
    if not json_page:
        break
    followers_list.append(json_page)
    contador += 1
followers_name = []
for page in followers_list:
    for follower in page:
        followers_name.append(follower['login'])
followers = pd.DataFrame()
followers['name'] = followers_name
followers.to_csv('followers_amazon.csv')
