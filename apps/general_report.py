import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
# import glob
import datetime

import plotly.graph_objs as go
from app import app


from plotly.subplots import make_subplots


given_date = pd.read_csv("./World/WorldSummary/Europe/Europe_summary.csv").iloc[-1]['Date']

african_summary = pd.read_csv('./World/WorldSummary/Africa/Africa_summary.csv', encoding='utf-8')

active_report = pd.read_csv('./DayReport/COVID19DailyReport.csv', encoding='utf-8')
last_new_report_date = pd.read_csv('./World/LastNewCaseReport/LastNewCaseReport.csv', encoding='utf-8')

# FUNCTIONS COLLECTION
if '_' in given_date:
    given_date = datetime.datetime.strptime(given_date[:-7], '%b').strftime("%B") + ' ' + given_date[
                                                                                          -7:-5] + ', ' + given_date[
                                                                                                          -4:]
else:
    given_date = given_date[:-2] + ' ' + given_date[-2:] + ', ' + str(2020)


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') + '-' + x[-7:-5] + '-' + x[
                                                                                                      -4:] if '_' in x else datetime.datetime.strptime(
        x[:-2], "%B").strftime('%b') + '-' + x[-2:] + '-' + '2020' for x in list_date]
    return x_date_format


# Date format for pie chart
def pie_date_format(col_date_str):
    if '_' in col_date_str:
        col_date = datetime.datetime.strptime(col_date_str[:-7], '%b').strftime('%b') + '-' + col_date_str[
                                                                                              -7:-5] + '-' + col_date_str[
                                                                                                             -4:]
    else:
        col_date = datetime.datetime.strptime(col_date_str[:-2], '%B').strftime('%b') + '-' + col_date_str[
                                                                                              -2:] + '-' + '2020'

    return col_date


date_val = datetime.datetime.strptime(given_date, "%B %d, %Y")
date_val = date_val.strftime('%d') + date_val.strftime('%m') + date_val.strftime('%Y')
date_file = "DailyCases" + str(date_val) + ".csv"

countries_new_cases = pd.read_csv('World/NewCases/' + date_file)

dates = countries_new_cases.columns.to_list()
dates = dates[1:]

# LOAD New Recovery Files
##################################
NRnew_recovered = pd.read_csv('WorldNR/NewRecovered/' + 'NewRecovered' + str(date_val) + ".csv")
NRnew_cases = pd.read_csv('WorldNR/NewCases/' + 'NewCases' + str(date_val) + ".csv")
NRnew_deaths = pd.read_csv('WorldNR/NewDeaths/' + 'NewDeaths' + str(date_val) + ".csv")
NRdates = NRnew_cases.columns.to_list()
NRdates = NRdates[1:]
##################################




# COLORS COLLECTION
colors = {'background': '#1d1160', 'text': 'cyan', 'crimson': '#DC143C', 'paragraphcolor': 'white'}

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label('Select Country:', style={'paddingTop': '.3rem'}),
            dcc.Dropdown(id='countries_new_cases_graph_names',
                            clearable=False,
                            options=[{'label': i, 'value': i} for i in
                                     countries_new_cases['Country_Other'].sort_values(ascending=True).unique()],
                            value="South Africa",
                            style={'fontSize': '18px', 'fontWeight': 'bold',}

        )], xs=11, sm=11, md=11, lg=3, xl=3),

        dbc.Col([ html.H3(id='tot_cases', style={'fontWeight': 'bold', 'color': '#00FFFF','fontSize': '20px'}),
            html.Label('Total Cases', style={'paddingTop': '.3rem'})],style={'backgroundColor': '#282828', 'borderRadius': '10px'}, className="label_display_result", width={'size': 'auto', 'offset':1}),
        dbc.Col([html.H3(id='tot_recovery', style={'fontWeight': 'bold','fontSize': '20px'}),
            html.Label('Total Recovery', style={'paddingTop': '.3rem'})], style={'backgroundColor': '#282828', 'borderRadius': '10px'},className="label_display_result", width={'size': 'auto', 'offset':1 }),
        dbc.Col([html.H3(id='tot_deaths', style={'fontWeight': 'bold', 'color': '#f73600','fontSize': '20px'}),
            html.Label('Total Deaths', style={'paddingTop': '.3rem'})],style={'backgroundColor': '#282828', 'borderRadius': '10px'}, className="label_display_result", width={'size': 'auto', 'offset':1 }),
        dbc.Col([html.H3(id='no_of_days', style={'fontWeight': 'bold', 'color': '#FFFF00','fontSize': '20px'}),
            html.Label('Last new case date', style={'paddingTop': '.3rem'})], style={'backgroundColor': '#282828', 'borderRadius': '10px'}, className="label_display_result", width={'size':'auto','offset':1}),
    ]),
    html.Br(),

dbc.Row(
        [
            dbc.Col(

            dcc.Graph('countries_new_cases_graph'),
                xs=11, sm=11, md=11, lg=6, xl=6
        ),
        dbc.Col(
            dcc.Graph('countries_wave_report'),
            xs=11, sm=11, md=11, lg=6, xl=6
        )
        ],
        # no_gutters=True,
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph('new_recovery_graph'),
            xs=12, sm=12, md=12, lg=12, xl=12)
        ]
    ),
    # dbc.Row([
    #     dbc.Col(
    #     html.Label('Ray Eke (Ceenuggets@gmail.com)'),   width={'size':'auto','offset':7}),
    #     html.Br(),
    #     # html.Label('Data Source'),
    #     html.A('Data Source: Worldometers daily updates', href='https://www.worldometers.info/coronavirus/#nav-yesterday', target="_blank")
    # ]),
#New Row

])


@app.callback(
    Output('countries_new_cases_graph', 'figure'),
    Output('countries_wave_report', 'figure'),
    Output('tot_cases', 'children'),
    Output('tot_recovery', 'children'),
    Output('tot_deaths', 'children'),
    Output('no_of_days', 'children'),
    Output('new_recovery_graph', 'figure'),
    [Input('countries_new_cases_graph_names', 'value')]
)
def country_new_cases(country_name):
    country = countries_new_cases[countries_new_cases['Country_Other'] == country_name]
    fig = go.Figure()
    fig2 = go.Figure()
    country_day_total = active_report.loc[active_report['Country_Other'] == country_name]['Total_Cases']
    country_tot_recovery = active_report.loc[active_report['Country_Other'] == country_name]['Total_Recovered']
    country_tot_deaths = active_report.loc[active_report['Country_Other'] == country_name]['Total_Deaths']
    country_last_case_date = last_new_report_date.loc[last_new_report_date['Country_Other'] == country_name]['Last_New_Case_Report_Date']
    country_total_per_day = []
    for date in dates:
        total = country[date].str.replace('+','', regex=False).str.replace(',','', regex=False).fillna(0).astype(int)
        country_total_per_day.append(int(total))

    fig.add_trace(
        go.Bar(x=format_date(dates[-20:]), y=country_total_per_day[-20:], text=country_total_per_day[-20:], textposition='outside',
               name=country_name, marker=dict(color='#32cd32', )))

    fig2.add_trace(
        go.Scatter(x=format_date(dates), y=country_total_per_day,  mode='lines', marker=dict(color='cyan', ))
    )
    fig.update_layout(
        height=550,
        template='plotly_dark',
        title={
            'text': country_name.upper() + "- COVID19 DAILY NEW CASES",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD')),
        yaxis=dict(title='<b>New Cases</b>', titlefont_size=18),
        xaxis_tickangle=90,
    )
    fig2.update_layout(
        height=550,
        template='plotly_dark',
        title={
            'text': country_name.upper() + "- COVID19 DAILY NEW CASES",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD'),nticks=15),
        yaxis=dict(title='<b>New Cases</b>', titlefont_size=18),
        xaxis_tickangle=90,
    )

    # New Recovered data
    #########################
    NRcountry_new_cases = NRnew_cases[NRnew_cases['Country_Other'] == country_name]
    NRcountry_new_recovery = NRnew_recovered[NRnew_recovered['Country_Other'] == country_name]
    NRcountry_new_deaths = NRnew_deaths[NRnew_deaths['Country_Other'] == country_name]
    fig3 = go.Figure()
    NRcountry_total_new_cases_per_day = []
    NRcountry_total_new_recovery_per_day = []
    NRcountry_total_new_deaths_per_day = []

    for date in NRdates:
        if NRcountry_new_cases[date].values[0] == 0:
            NRnew_cases_total = NRcountry_new_cases[date].values[0]
            NRcountry_total_new_cases_per_day.append(int(NRnew_cases_total))
        else:
            NRnew_cases_total = NRcountry_new_cases[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(0).astype(
                int)
            NRcountry_total_new_cases_per_day.append(int(NRnew_cases_total))

        if NRcountry_new_recovery[date].values[0] == 0:
            NRnew_recovery_total = NRcountry_new_recovery[date].values[0]
            NRcountry_total_new_recovery_per_day.append(int(NRnew_recovery_total))
        else:
            NRnew_recovery_total = NRcountry_new_recovery[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(
                0).astype(int)
            NRcountry_total_new_recovery_per_day.append(int(NRnew_recovery_total))

        if NRcountry_new_deaths[date].values[0] == 0:
            NRnew_deaths_total = NRcountry_new_deaths[date].values[0]
            NRcountry_total_new_deaths_per_day.append(int(NRnew_deaths_total))
        else:
            # NRnew_deaths_total = NRcountry_new_deaths[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(0).astype(
            #     int)
            NRcountry_new_deaths.fillna(0, inplace=True)
            NRnew_deaths_total = NRcountry_new_deaths[date].replace("[+,]", "", regex=True)
            NRcountry_total_new_deaths_per_day.append(int(NRnew_deaths_total))

    fig3.add_trace(
        go.Bar(x=format_date(NRdates[-10:]), y=NRcountry_total_new_cases_per_day[-10:], text=NRcountry_total_new_cases_per_day[-10:],
               textposition='outside', name='New Cases', marker=dict(color='teal', )))
    fig3.add_trace(
        go.Bar(x=format_date(NRdates[-10:]), y=NRcountry_total_new_recovery_per_day[-10:], text=NRcountry_total_new_recovery_per_day[-10:],
               textposition='outside', name='New Recovery', marker=dict(color='#f0a150', )))
    fig3.add_trace(
        go.Bar(x=format_date(NRdates[-10:]), y=NRcountry_total_new_deaths_per_day[-10:], text=NRcountry_total_new_deaths_per_day[-10:],
               textposition='outside', name='New Deaths', marker=dict(color='crimson', )))
    fig3.update_layout(template='plotly_dark',
                       barmode='group',
                       height=550,
                       title={
                           'text': country_name.upper() + "- COVID19 NEW CASES, RECOVERIES AND DEATHS",
                           'y': 0.9,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                       xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD'), nticks=15),
                       yaxis=dict(title='<b>Cases</b>', titlefont_size=18),
                       xaxis_tickangle=90),
    #########################

    return fig, fig2, country_day_total, country_tot_recovery, country_tot_deaths, country_last_case_date, fig3


