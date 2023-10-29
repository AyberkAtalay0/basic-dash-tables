# Module Imports
from dash import register_page, html
import dash_mantine_components as dmc
from os import listdir
import pandas as pd
from unidecode import unidecode as ud

# App
register_page(__name__, path="/sinav", path_template="sinav/<ogr_yili>_<sinav_no>", title="MHAL Panel")

def layout(ogr_yili, sinav_no):
    df_path, df = None, None
    try:
        for i in listdir(f"database\\{ogr_yili}"):
            if float(str(sinav_no).strip()) == float(str(i.split(" - ")[0]).strip()): df_path = f"database\\{ogr_yili}\\{i}"
        if df_path != None: df = pd.read_excel(df_path)
    except: df_path, df = None, None

    df_title = ogr_yili + " " + df_path.split("/")[-1].split(" - ")[-1].removesuffix(".xlsx") if df_path != None else "Sınav Bulunamadı"
    table = []
    if type(df) != type(None):
        for r in range(len(df.index)):
            row = df.loc[r, :].values.flatten().tolist()[1:]
            table.append(html.Tr([html.Td(str(row[-4]))] + [html.Td(str(i)) for i in row] + [html.A(dmc.Button("Profil"), href=f"/ogrenci/{row[0]}_{ud(row[1].lower().replace(' ',''))}")]))
    
    return html.Div(children=[
        html.Div(children=[
            html.Div([html.H1(df_title), html.A(dmc.Button("Ana Sayfaya Dön"), href="/", style={"margin-top": "30px"})], style={"display": "flex", "justify-content": "space-between"}),
            html.Br(),
            dmc.Card(children=[
                html.H3("Kurum Sonuçları"),
                dmc.ScrollArea(children=[
                    dmc.Table(children=[
                        html.Thead(
                            html.Tr([
                                html.Th("Sıra"),
                                html.Th("Numara"),
                                html.Th("İsim"),
                                html.Th("Sınıf"),
                                html.Th("D (Toplam)"), html.Th("Y (Toplam)"), html.Th("N (Toplam)"), 
                                html.Th("D (Türkçe)"), html.Th("Y (Türkçe)"), html.Th("N (Türkçe)"),
                                html.Th("D (Sosyal)"), html.Th("Y (Sosyal)"), html.Th("N (Sosyal)"),
                                html.Th("D (Matematik)"), html.Th("Y (Matematik)"), html.Th("N (Matematik)"),
                                html.Th("D (Fen)"), html.Th("Y (Fen)"), html.Th("N (Fen)"),
                                html.Th("Kurum"),
                                html.Th("İlçe"),
                                html.Th("İl"),
                                html.Th("Genel"),
                            ])
                        ),
                        html.Tbody(children=table, id="ogrenci-sinav-table"),
                    ], highlightOnHover=True, withBorder=True, style={"zoom": "80%"})
                ], offsetScrollbars=False, style={"height": "900px"}),
            ], style={"width": "100%", "padding-left": "20px", "padding-right": "20px", "padding-bottom": "20px", "margin-bottom": "30px"}, withBorder=True)
        ], style={"width": "100%", "padding-top": "20px", "padding-left": "6%", "padding-right": "6%", "padding-bottom": "20px"})
    ], style={"margin-left": "0px"})