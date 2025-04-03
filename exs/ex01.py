import requests

r = requests.get('https://api.github.com/users/meu_gh')
print(r.status_code)
json_do_meu_perfil = r.json()
print(json_do_meu_perfil)
print(r.url)
print(json_do_meu_perfil['login'])
print(json_do_meu_perfil['name'])
print(json_do_meu_perfil['public_repos'])
print(json_do_meu_perfil['created_at'])
