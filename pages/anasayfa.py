# Module Imports
from dash import register_page, html
import dash_mantine_components as dmc
from os import listdir

# App
register_page(__name__, path="/", title="MHAL Panel")

def layout():
    return html.Div(children=[
    html.Div(children=[
        html.H1("Ana Sayfa"),
        html.Br(),
        dmc.Card(children=[
            html.H3("Sınav Sorgu"),
            html.H5("Öğretim Yılı", style={"margin-bottom": "4px"}),
            dmc.Select(placeholder="Select", id="sorgu-ogretim-yili", value=listdir("database")[-1], data=[{"value":i, "label":i} for i in listdir("database")]),
            html.Br(),
            html.H5("Sınav İndisi", style={"margin-bottom": "4px"}),
            dmc.Select(placeholder="Select", id="sorgu-sinav-indisi", value=listdir("database\\"+listdir("database")[-1])[-1], data=[{"value":i, "label":i.removesuffix(".xlsx")} for i in listdir("database\\"+listdir("database")[-1])]),
            html.Br(),
            html.A(dmc.Button("Getir", style={"width": "100%"}), href="sinav/x_x", id="sorgu-sinav-getir")
        ], style={"width": "100%", "padding-left": "20px", "padding-right": "20px", "padding-bottom": "20px", "margin-bottom": "30px"}, withBorder=True),
        dmc.Card(children=[
            html.H3("Öğrenci Sorgu"),
            html.H5("Öğrenci Adı (Opsiyonel)", style={"margin-bottom": "4px"}),
            dmc.TextInput(id="sorgu-ogrenci-adi"),
            html.Br(),
            html.H5("Öğrenci Numarası (Opsiyonel)", style={"margin-bottom": "4px"}),
            dmc.TextInput(id="sorgu-ogrenci-numarasi"),
            html.Br(),
            html.H5("Öğrenci Sınıfı", style={"margin-bottom": "4px"}),
            dmc.Select(placeholder="Select", id="sorgu-ogrenci-sinifi", value=12, data=[{"value":11, "label":11}, {"value":12, "label":12}]),
            html.Br(),
            dmc.Button("Filtrele", id="sorgu-ogrenci-filtrele", style={"width": "100%"}),
            html.Br(),
            html.Br(),
            html.Br(),
            dmc.ScrollArea(children=[
                dmc.Table(
                    [
                        html.Thead(html.Tr([html.Th("Numara"), html.Th("İsim"), html.Th("Sınıf")])),
                        html.Tbody([], id="sorgu-ogrenci-table")
                    ],
                    highlightOnHover=True,
                    withBorder=True,
                    striped=True,
                    verticalSpacing=10,
                    style={"zoom": "80%"}
                )
            ], offsetScrollbars=False, style={"height": "720px"}),
        ], style={"width": "100%", "padding-left": "20px", "padding-right": "20px", "padding-bottom": "20px", "margin-bottom": "30px"}, withBorder=True),
    ], style={"width": "100%", "padding-top": "20px", "padding-left": "6%", "padding-right": "6%", "padding-bottom": "20px"})
], style={"margin-left": "0px"})