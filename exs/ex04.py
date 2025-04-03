import requests

api_url_base = 'https://api.github.com'
owner = 'amzn'
repo_forked = 'sid-provision'
url = f'{api_url_base}/repos/{owner}/{repo_forked}/forks'
headers = {
    'Authorization': 'Bearer meu_token',
    'X-GitHub-Api-Version': '2022-11-28'
}

r = requests.post(url=url, headers=headers)
print(r)
