# Module Imports
from dash import register_page, html, dcc
import dash_mantine_components as dmc
from os import listdir, path
import pandas as pd
from unidecode import unidecode as ud

# App
register_page(__name__, path="/ogrenci", path_template="ogrenci/<ogr_no>_<ogr_name>", title="MHAL Panel")

def get_rows1(i):
    out = []
    for y in listdir(path.join("database")):
        for x in listdir(path.join("database", y)):
            if x.endswith(".xlsx"):
                df = pd.read_excel(path.join("database", y, x))
                r = None
                for id, di in enumerate(df["İsim"].tolist()):
                    if ud(str(di).lower().replace(" ","")) == ud(str(i).lower().replace(" ","")): r = id
                if r != None: 
                    al = df.iloc[r].tolist()
                    for ai in range(len(al)):
                         if "bilinmiyor" in str(al[ai]).lower(): al[ai] = "12 / X"
                    out.append(al+[x.removesuffix(".xlsx")+" "+y])
    numaralar = [o[1] for o in out if float(o[1]) > 0]
    if len(numaralar) == 0: numaralar.append(0)
    isimler = [o[2] for o in out]
    siniflar = [o[3] for o in out]
    saltsiniffix = max([int(float(sin[3].split("/")[0])) for sin in out])
    numfix = max(set(numaralar), key=numaralar.count)
    isimfix = max(set(isimler), key=isimler.count)
    siniffix = max(set(siniflar), key=siniflar.count)
    for z in range(len(out)):
        out[z][1] = numfix
        out[z][2] = isimfix
        if siniffix.startswith(str(saltsiniffix)): out[z][3] = siniffix
        else: out[z][3] = f"{saltsiniffix} / {siniffix[-1]}"
    return out

def layout(ogr_no, ogr_name):
    rows = get_rows1(ogr_name)

    numara = rows[0][1]
    isim = rows[0][2]
    sinif = rows[0][3]
    
    return html.Div(children=[
        html.Div(children=[
            html.Div([html.H1("Öğrenci"), html.A(dmc.Button("Ana Sayfaya Dön"), href="/", style={"margin-top": "30px"})], style={"display": "flex", "justify-content": "space-between"}),
            html.Br(),
            dmc.Card(children=[
                html.H3("Öğrenci Bilgileri"),
                dmc.Table(children=[
                    html.Thead(html.Tr([html.Th("Öğrenci Adı"), html.Th("Öğrenci Sınıfı"), html.Th("Öğrenci Numarası")])),
                    html.Tbody(children=[html.Tr([html.Td(isim, id="ogrenci-bilgi-isim"), html.Td(sinif, id="ogrenci-bilgi-sinif"), html.Td(numara, id="ogrenci-bilgi-numara")])], id="ogrenci-table"),
                ], highlightOnHover=False, withBorder=True)
            ], style={"width": "100%", "padding-left": "20px", "padding-right": "20px", "padding-bottom": "20px", "margin-bottom": "30px"}, withBorder=True),
            dmc.Card(children=[
                html.H3("Sonuç Sorgu"),
                html.H5("Öğretim Yılı", style={"margin-bottom": "4px"}),
                dmc.Select(placeholder="Select", id="sonuc-ogretim-yili", value=listdir(path.join("database"))[-1], data=[{"value":i, "label":i} for i in listdir(path.join("database"))]),
                html.Br(),
                dmc.Button("Getir", id="sonuc-sorgu-getir", style={"width": "100%"}),
                html.Br(),
                html.Br(),
                dmc.ScrollArea(children=[
                    dmc.Table(children=[
                        html.Thead(
                            html.Tr([
                                html.Th("Sınav"),
                                html.Th("Sıra"),
                                html.Th("D (Toplam)"), html.Th("Y (Toplam)"), html.Th("N (Toplam)"), 
                                html.Th("D (Türkçe)"), html.Th("Y (Türkçe)"), html.Th("N (Türkçe)"),
                                html.Th("D (Sosyal)"), html.Th("Y (Sosyal)"), html.Th("N (Sosyal)"),
                                html.Th("D (Matematik)"), html.Th("Y (Matematik)"), html.Th("N (Matematik)"),
                                html.Th("D (Fen)"), html.Th("Y (Fen)"), html.Th("N (Fen)"),
                                html.Th("Kurum"),
                                html.Th("İlçe"),
                                html.Th("İl"),
                                html.Th("Genel")
                            ])
                        ),
                        html.Tbody(children=[], id="sonuc-ogrenci-table"),
                    ], highlightOnHover=False, withBorder=True, style={"zoom": "80%"})
                ], offsetScrollbars=False),
                html.Br(),
                html.Br(),
                html.H5("Ders Bazlı Netler", style={"margin-bottom": "4px"}),
                dcc.Graph(id="ogrenci-net-chart", config={"displayModeBar": False}, figure={"data": [{"x": [], "y": [], "type": "bar", "name": ""}], "layout": {"title": "Veri Yok", "plot_bgcolor": "#25262B", "paper_bgcolor": "#25262B", "font": {"color": "#DFDFDF"}, "margin": dict(l=0, r=0, t=0, b=50),}}),
                html.Br(),
                html.Br(),
                html.H5("Sınav Puanları", style={"margin-bottom": "4px"}),
                dcc.Graph(id="ogrenci-puan-chart", config={"displayModeBar": False}, figure={"data": [{"x": [], "y": [], "type": "bar", "name": ""}], "layout": {"title": "Veri Yok", "plot_bgcolor": "#25262B", "paper_bgcolor": "#25262B", "font": {"color": "#DFDFDF"}, "margin": dict(l=0, r=0, t=0, b=50),}}),
            ], style={"width": "100%", "padding-left": "20px", "padding-right": "20px", "padding-bottom": "20px", "margin-bottom": "30px"}, withBorder=True)
        ], style={"width": "100%", "padding-top": "20px", "padding-left": "6%", "padding-right": "6%", "padding-bottom": "20px"})
    ], style={"margin-left": "0px"})
