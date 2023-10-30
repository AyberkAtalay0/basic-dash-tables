# Module Imports
import base64, flask, os, dash_mantine_components as dmc
from dash import Dash, page_container, Output, Input, State, html
from dash_auth.auth import Auth
from datetime import datetime
from os import listdir
import pandas as pd
from unidecode import unidecode as ud

# Logs
# log = logging.getLogger("werkzeug")
# log.setLevel(logging.WARNING)

# Auth
class MHALAuth(Auth):
    def __init__(self, app):
        Auth.__init__(self, app)

    def is_authorized(self):
        out = {}
        if os.path.exists("configuration\\users.cfg"):
            with open("configuration\\users.cfg", "r", encoding="utf-8") as f:
                for raw in f.read().removesuffix("\n").strip().split("\n"):
                    user = raw.split(";")
                    out.update({user[0]: user[1].replace("<secret1>", str(int(float(datetime.now().month*datetime.now().day+3))))})
        else:
            with open("configuration\\users.cfg", "w") as f: f.write("")

        self._users = (
            out
            if isinstance(out, dict)
            else {k: v for k, v in out}
        )

        header = flask.request.headers.get("Authorization", None)
        if not header:
            return False
        username_password = base64.b64decode(header.split("Basic ")[1])
        username_password_utf8 = username_password.decode("utf-8")
        username, password = username_password_utf8.split(":", 1)
        return self._users.get(username) == password

    def login_request(self):
        return flask.Response(
            "Login Required",
            headers={"WWW-Authenticate": 'Basic realm="User Visible Realm"'},
            status=401
        )

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap

# App
app = Dash(__name__, use_pages=True, serve_locally=True, title="MHAL Panel", update_title="MHAL Panel", meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0,"}])
auth = MHALAuth(app)
app._favicon = "favicon.png"

app.layout = dmc.MantineProvider(
    children=[
        page_container,

        html.Div(id="none", style={"display": "none"}),
    ],
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    withCSSVariables=True
)

# Callbacks
@app.callback(
    Output("sorgu-sinav-indisi", "data"), Output("sorgu-sinav-indisi", "value"), 
    Input("sorgu-ogretim-yili", "value")
)
def indis_yenile(ogretim_yili):
    return listdir("database\\"+ogretim_yili), listdir("database\\"+ogretim_yili)[-1] if len(listdir("database\\"+ogretim_yili)) > 0 else None

@app.callback(
    Output("sorgu-sinav-getir", "href"), 
    Input("sorgu-sinav-indisi", "value"),
    State("sorgu-ogretim-yili", "value")
)
def sinav_getir(indi, ogr_yili):
    try: return f"sinav/{ogr_yili}_{indi.split(' - ')[0]}"
    except: return "sinav/x_x"

@app.callback(
    Output("sorgu-ogrenci-table", "children"),
    Input("sorgu-ogrenci-filtrele", "n_clicks"),
    State("sorgu-ogrenci-adi", "value"), State("sorgu-ogrenci-numarasi", "value"), State("sorgu-ogrenci-sinifi", "value")
)
def ogrenci_filtrele(n_clicks, ograd, ogrno, ogrsn):
    out, readies, order = [], [], []
    for ogry in listdir("database"):
        for xlsx in listdir("database\\"+ogry):
            if xlsx.endswith(".xlsx"):
                table = pd.read_excel("database\\"+ogry+"\\"+xlsx)
                for numara, isim, sinif in zip(table["Numara"], table["İsim"], table["Sınıf"]):
                    if (ud(str(ograd).replace("None","").replace(" ","").upper()) in ud(str(isim).replace(" ","").upper()) or ud(str(ograd).replace("None","").replace(" ","").upper()) == "") \
                        and (ud(str(ogrno).replace("None","").replace(" ","").upper()) in ud(str(numara).replace(" ","").upper()) or ud(str(ogrno).replace("None","").replace(" ","").upper()) == "") \
                            and (ud(str(ogrsn).replace("None","").replace(" ","").upper()) in ud(str(sinif).replace(" ","").upper()) or ud(str(ogrsn).replace("None","").replace(" ","").upper()) == ""):
                        if isim.split()[0].strip() == isim.strip(): isim = isim + " X"
                        elem = html.Tr([html.Td(str(numara)), html.Td(isim.upper()), html.Td(sinif), html.A(children=dmc.Button("Profil"), href=f"/ogrenci/{numara}_{ud(isim.lower().replace(' ',''))}")])
                        if not (numara, isim, sinif) in readies:
                            out.append(elem)
                            readies.append((numara, isim, sinif))
                            order.append(numara)
    return [x for _, x in sorted(zip(order, out), key=lambda pair: pair[0])]

def get_rows2(i, y):
    out = []
    for x in listdir(f"database\\{y}"):
        if x.endswith(".xlsx"):
            df = pd.read_excel(f"database\\{y}\\{x}")
            r = None
            for id, di in enumerate(df["İsim"].tolist()):
                if ud(di.lower().replace(" ","")) == ud(i.lower().replace(" ","")): r = id
            if r != None: out.append([x.removesuffix(".xlsx")+" "+y]+df.iloc[r].tolist())
    for o in range(len(out)):
        del out[o][2]
        del out[o][2]
        del out[o][2]
    return out

@app.callback(
    Output("sonuc-ogrenci-table", "children"), Output("ogrenci-net-chart", "figure"), Output("ogrenci-puan-chart", "figure"),
    Input("sonuc-sorgu-getir", "n_clicks"),
    State("sonuc-ogretim-yili", "value"), State("ogrenci-bilgi-isim", "children"), State("ogrenci-bilgi-sinif", "children"), State("ogrenci-bilgi-numara", "children")
)
def sonuc_getir(n_clicks, ogr_yili, isim, sinif, numara):
    rows = get_rows2(isim, ogr_yili)

    table = [html.Tr([html.Td(str(i)) for i in row] + [html.A(dmc.Button("Tablo"), href=f"/sinav/{ogr_yili}_{str(row[0]).split(' - ')[0].strip()}")]) for row in rows]

    net_fig = {
        "data": [
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[4]) for row in rows], "text": [str(float(row[4])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Toplam"},
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[7]) for row in rows], "text": [str(float(row[7])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Türkçe"},
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[10]) for row in rows], "text": [str(float(row[10])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Sosyal"},
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[13]) for row in rows], "text": [str(float(row[13])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Matematik"},
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [float(row[16]) for row in rows], "text": [str(float(row[16])) for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "bar", "name": "Fen"},
        ],
        "layout": {
            "plot_bgcolor": "#25262B",
            "paper_bgcolor": "#25262B",
            "font": {"color": "#DFDFDF"},
            "margin": dict(l=0, r=0, t=0, b=50),
            "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            "xaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
            "yaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
        }
    }

    puan_fig = {
        "data": [
            {"x": [ud(row[0].split("(")[-1].split(")")[0].strip()) for row in rows], "y": [round(float(row[7])*3.3 + float(row[10])*3.4 + float(row[13])*3.3 + float(row[16])*3.4 + 100, 3)  for row in rows], "text": [str(round(float(row[7])*3.3 + float(row[10])*3.4 + float(row[13])*3.3 + float(row[16])*3.4 + 100, 3))  for row in rows], "hovertext": [ud(row[0].split("-")[1].split("(")[0].strip()) for row in rows], "type": "marker", "name": "Puan"},
        ],
        "layout": {
            "plot_bgcolor": "#25262B",
            "paper_bgcolor": "#25262B",
            "font": {"color": "#DFDFDF"},
            "margin": dict(l=0, r=0, t=0, b=50),
            "legend": dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            "xaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
            "yaxis": {"fixedrange": True, "rangeslider": {"visible": True}},
        }
    }
    return table, net_fig, puan_fig

if __name__ == "__main__":
    app.run_server(debug=False, port=5000)
