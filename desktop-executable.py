import requests
branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
desktop_code = "\n".join(requests.get(branch_url+"/desktop-source.py").json()["payload"]["blob"]["rawLines"]).replace("\r", "")
exec(desktop_code)