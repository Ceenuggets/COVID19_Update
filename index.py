from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
import pandas as pd
import datetime
from app import server

from apps import general_report, all_continents, collection, covid19_deaths

given_date = pd.read_csv("World/WorldSummary/Europe/Europe_summary.csv").iloc[-1]['Date']

# FUNCTIONS COLLECTION
if '_' in given_date:
    given_date = datetime.datetime.strptime(given_date[:-7], '%b').strftime("%B") + ' ' + given_date[
                                                                                          -7:-5] + ', ' + given_date[
                                                                                                          -4:]
else:
    given_date = given_date[:-2] + ' ' + given_date[-2:] + ', ' + str(2020)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row(

            dbc.Col(html.Div(children=
            [
                html.H3(children='COVID19 REPORT', style={'fontWeight': 'bold'}),
                html.H6(children=  'for ' + given_date , style={'marginTop': '-10px', 'marginBottom': '10px','color': '#00FFFF'}),
             ], style={'textAlign': 'center', 'padding': '1rem'}))),
    ]),
    # html.Div([
    #         dcc.Link('Home | ', href='/apps/general_report'),
    #         dcc.Link('General | ', href='/apps/all_continents'),
    #         dcc.Link('More.. ', href='/apps/collection'),
    # ]),
dbc.Row([
    dbc.Col([
dbc.Nav(
    [
        dbc.NavLink("Home", active=True, href="/apps/general_report", style={'color': 'Orange','fontWeight': 'bold',
            'textDecoration': 'underline', 'fontSize': '20px'}),
        dbc.NavLink("General", href="/apps/all_continents", style={'color': 'Orange','fontWeight': 'bold',
            'textDecoration': 'underline', 'fontSize': '20px'}),
        dbc.NavLink("COVID19 Deaths", href="/apps/covid19_deaths", style={'color': 'Orange','fontWeight': 'bold',
            'textDecoration': 'underline', 'fontSize': '20px'}),
        dbc.NavLink("More..", href="/apps/collection", style={'color': 'Orange','fontWeight': 'bold',
            'textDecoration': 'underline', 'fontSize': '20px'}),

    ]),
 ],width={'size': 8, 'offset': 2}),

]),

html.Br(),


    html.Div(id='page_content', children=[]),

html.Br(),

dbc.Row([
        dbc.Col(
        html.Label('Ray Eke (Ceenuggets@gmail.com)'),   width={'size':'auto','offset':7}),
        html.Br(),
        # html.Label('Data Source'),
        html.A('Data Source: Worldometers daily updates', href='https://www.worldometers.info/coronavirus/#nav-yesterday', target="_blank")
    ]),


])


@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
    )
def show_page(pathname):
    if pathname == '/apps/general_report':
        return general_report.layout
    if pathname == '/apps/all_continents':
        return all_continents.layout
    if pathname == '/apps/collection':
        return collection.layout
    if pathname == '/apps/covid19_deaths':
        return covid19_deaths.layout
    else:
        return general_report.layout


if __name__ == '__main__':
    app.run_server(debug=True)
