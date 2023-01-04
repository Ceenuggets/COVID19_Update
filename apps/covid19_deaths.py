import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from dash import dash_table as dt
import calendar
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app


given_date = pd.read_csv("./World/WorldSummary/Europe/Europe_summary.csv").iloc[-1]['Date']

if '_' in given_date:
    given_date = datetime.datetime.strptime(given_date[:-7], '%b').strftime("%B") + ' ' + given_date[
                                                                                          -7:-5] + ', ' + given_date[
                                                                                                          -4:]
else:
    given_date = given_date[:-2] + ' ' + given_date[-2:] + ', ' + str(2020)

#  GET RIGHT CSV FILE NAME FORMAT
date_val = datetime.datetime.strptime(given_date, "%B %d, %Y")
date_val = date_val.strftime('%d')+date_val.strftime('%m')+date_val.strftime('%Y')
date_file ="NewDeaths"+str(date_val)+".csv"


covid_record  = pd.read_csv('./World/NewDeaths/' + date_file)
countries = covid_record['Country_Other']
countries = countries[1:]


day_of_month = int(datetime.datetime.strptime(date_file[-12:-4], '%d%m%Y').strftime('%d'))

#First20 country deaths
new_daily_deaths =  covid_record
latest_cases_column_values = new_daily_deaths.iloc[:, -1]
latest_cases_column_values = list(latest_cases_column_values)
##################Modification for the occasional floats in new deaths#########################
latest_cases_column = [type(x) for x in latest_cases_column_values]
# print(latest_cases_column)
if float in latest_cases_column:
    # new_daily_deaths = new_daily_deaths.copy()
    new_daily_deaths.fillna(0, inplace=True)
    # new_daily_deaths.iloc[:, -1] = new_daily_deaths.iloc[:, -1].str.replace(',', '', regex=False).fillna(0).str.replace(
    #     '+', '', regex=False).fillna(0).str.replace('.0', '', regex=False).fillna(0).astype(int)
    new_daily_deaths.iloc[:, -1] = new_daily_deaths.iloc[:, -1].replace("[+,.0]", "", regex=False).astype(int)
else:
    new_daily_deaths.iloc[:, -1] = new_daily_deaths.iloc[:, -1].str.replace(',', '', regex=False).fillna(0).str.replace(
        '+', '', regex=False).fillna(0).str.replace('.0', '', regex=False).fillna(0).astype(int)

#################end of modification###########################

# new_daily_deaths.iloc[:, -1] = new_daily_deaths.iloc[:, -1].str.replace(',', '', regex=False).fillna(0).str.replace('+', '', regex=False).fillna(0).str.replace('.0', '', regex=False).fillna(0).astype(int)


#######################
# new_daily_deaths = new_daily_deaths.copy()
# new_daily_deaths.fillna(0, inplace=True)
# new_daily_deaths.iloc[:, -1] = new_daily_deaths.iloc[:, -1].replace("[+,.0]", "", regex=False).astype(int)
######################
new_daily_deaths_first20 = new_daily_deaths.sort_values(new_daily_deaths.iloc[:,-1].name, ascending=False)[1:]
new_daily_deaths_first20 = new_daily_deaths_first20['Country_Other'][:20].tolist()
############################################

years = []
for year in covid_record.columns[1:]:
    if '_' in year:
        if year[-4:] not in years:
            years.append(year[-4:])
    else:
        actual_year = '2020'
        if actual_year not in years:
            years.append(actual_year)
months_option_list = [{'label': calendar.month_name[i], 'value': calendar.month_name[i]} for i in range(1, 13)]


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') +'-' + x[-7:-5]+'-'+x[-4:] if '_'in x  else  datetime.datetime.strptime(x[:-2], "%B").strftime('%b') +'-' +x[-2:]+'-' +'2020'  for x in list_date]
    return x_date_format


# #####for populating country graph#########
dates = covid_record.columns.to_list()
dates = dates[1:]

covid19_death_record =  covid_record.copy()
covid19_death_record.fillna(0, inplace=True)
covid19_death_record.set_index('Country_Other', inplace=True)
########################################################

# ##### generate graph for new countries selections
def genarate_new_country_graph(new_countries_selection):
    fig = go.Figure()
    for country in new_countries_selection:
        country_total_per_day = []
        for date in dates:
            if covid19_death_record.loc[[country], [date]][date].values == 0:
                total = covid19_death_record.loc[[country], [date]][date].values[0]
                country_total_per_day.append(int(total))
            else:
                total = str(covid19_death_record.loc[[country], [date]][date].values[0]).replace('+', '').replace(',','').replace('.0', '')
                country_total_per_day.append(int(total))

        fig.add_trace(go.Scatter(
            x=format_date(dates),
            y=country_total_per_day,
            name=country,
            mode='lines',
        ))
    if len(new_countries_selection) == 1:
        fig.update_layout(
            template='plotly_dark',
            height=550,
            width=1200,
            title={
                'text': '<b>' + 'COVID19 DEATHS - ' + new_countries_selection[0] + '</b>',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B'), nticks=30),
            yaxis=dict(title='<b>Number of Deaths</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B')),
            # yaxis_title="Deaths",
            xaxis_tickangle=90, )
    else:
        fig.update_layout(
            template='plotly_dark',
            height=550,
            width=1200,
            title={
                'text': '<b>' + 'COVID19 DEATHS ' + '</b>',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B'), nticks=30),
            yaxis=dict(title='<b>Number of Deaths</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B')),
            # yaxis_title="Deaths",
            xaxis_tickangle=90,)

    return fig
###############################################################


layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            html.Label('Select Countries', style={'paddingTop': '.3rem'}),
            dcc.Dropdown(
                id='select_countries',
                options=[{'label': str(i), 'value': str(i)} for i in countries.sort_values(ascending=True).unique()],
                multi=True,
                value=new_daily_deaths_first20[:20],
                # value=countries.sort_values(ascending=True).unique()[:4],
                # value = options[0]['label']
                style={'fontSize': '18px', 'fontWeight': 'bold',}
                )], xs=11, sm=11, md=11, lg=6, xl=6

        ),
        dbc.Col([
            html.Label('Select year', style={'paddingTop': '.3rem'}),
            dcc.Dropdown(
                id='select_year',
                options=[{'label': str(i), 'value': str(i)} for i in sorted(years, reverse=True)],
                searchable=False,
                clearable=False,
                value=sorted(years, reverse=True)[0],
                style={'fontSize': '18px', 'fontWeight': 'bold',}
            )], xs=11, sm=11, md=11, lg=2, xl=2
        ),
        dbc.Col([
            html.Label('Select Month', style={'paddingTop': '.3rem'}),
            dcc.Dropdown(
                id='select_month',
                clearable=False,
                options=[{'label': calendar.month_name[i], 'value': calendar.month_name[i]} for i in range(1, 13)],
                value=[],
                style={'fontSize': '18px', 'fontWeight': 'bold',}
            )], xs=11, sm=11, md=11, lg=2, xl=2
        ),
        # dbc.Col([
        #         # html.Label('Click to display result', style={'paddingTop': '.3rem'}),
        #         html.Button(
        #         'Display Result',
        #         id='result_button',
        #         n_clicks=0,
        #     )], style={'marginTop': '35px'}, xs=6, sm=6, md=6, lg=2, xl=2
        # ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                id='div_display',
                 )
            ),  xs=11, sm=11, md=11, lg=11, xl=11
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='display_subplots',
                ),
                style={'height': '100%',}
            ), xs=11, sm=11, md=11, lg=11, xl=11
        ),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(html.Label(id="datatable_header", style={'backgroundColor': '#282828', 'borderRadius': '1px'}),
                     style={'textAlign': 'center', "color": "cyan", "fontWeight": "bold", 'paddingTop': '.1rem'}),
                     xs=11, sm=11, md=11, lg=11, xl=11)
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
            id='display_dataframe',
            # style={'width': '100%', 'backgroundColor': '#041E42'}
            ), xs=11, sm=11, md=11, lg=11, xl=11
        ),
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='display_country_graph',
                ),
                # style={'height': '100%',}
            ), xs=12, sm=12, md=11, lg=11, xl=11
        ),
    ]),


## Another Row
])


@app.callback(
    Output('select_month', 'options'),
    Output('select_month', 'value'),
    Input('select_year', 'value')
)
def load_month_for_2020(selected_year):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if selected_year is None:
        return dash.no_update
    elif selected_year == '2020':
        options = [{'label': calendar.month_name[i], 'value': calendar.month_name[i]} for i in range(4, 13)]
        value = options[-1]['label']
        # print(value)
        return options, value
    elif selected_year == str(current_year):
        options = [{'label': calendar.month_name[i], 'value': calendar.month_name[i]} for i in range(1, current_month+1)]
        value = options[-1]['label']
        # print(value)
        return options, value

    else:
        options = [{'label': calendar.month_name[i], 'value': calendar.month_name[i]} for i in range(1, 13)]
        value = options[-1]['label']
        # print(value)
        return options, value


@app.callback(
    Output('div_display', 'figure'),
    Output('display_subplots', 'figure'),
    Output('datatable_header', 'children'),
    Output('display_dataframe', 'children'),
    Input('select_countries', 'value'),
    Input('select_year', 'value'),
    Input('select_month', 'value'),

)
def covid19_deaths(chosen_countries, chosen_year, month):
    fig = go.Figure()
    selected_countries = []
    if chosen_countries is not None and chosen_year is not None and month is not None:
        country_daily_deaths_summary = pd.DataFrame()
        covid_deaths = covid_record.copy()
        chosen_month = datetime.datetime.strptime(month, '%B').strftime('%b')
        header = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') + '-' + x[-7:-5] + '-' + x[
                                                                                                   -4:] if '_' in x else datetime.datetime.strptime(
            x[:-2], "%B").strftime('%b') + '-' + x[-2:] + '-' + '2020' for x in covid_deaths.columns[1:]]
        header.insert(0, 'Country_Other')
        new_colname_dict = {i: j for i, j in zip(covid_deaths.columns, header)}
        covid_deaths.rename(columns=new_colname_dict, inplace=True)
        for country in chosen_countries:
            country_daily_deaths = covid_deaths.loc[covid_deaths['Country_Other'] == country]
            select_columns = [column for column in country_daily_deaths.columns if
                              chosen_month in column and chosen_year in column]
            country_daily_deaths = country_daily_deaths[select_columns]
            if country_daily_deaths_summary.empty:
                country_daily_deaths_summary['Date'] = country_daily_deaths.columns
                country_daily_deaths_summary[country] = country_daily_deaths.T.values
            else:
                country_daily_deaths_summary[country] = country_daily_deaths.T.values
        country_daily_deaths_summary2 = country_daily_deaths_summary
        data = country_daily_deaths_summary.to_dict('records')
        columns = [{"name": i, "id": i, "selectable": False, } if i == "Date" else {"name": i, "id": i, "selectable": True,} for i in country_daily_deaths_summary.columns]
        if len(chosen_countries) == 1:
            selected_countries = [chosen_countries[0]]
        elif len(chosen_countries) >= 2:
            selected_countries = chosen_countries[:2]
        ###################


        for country in country_daily_deaths_summary.columns[1:]:
            # for value in country_daily_deaths_summary[country].values:
            daily_cases = [0 if x == np.nan else str(x).replace('+', '').replace(',', '').replace('.0', '') for x in country_daily_deaths_summary[country].values]
            # daily_cases = [0 if x == np.nan else str(x).replace("[+,.0]", "") for x in country_daily_deaths_summary[country].values]
            # print(daily_cases)
            daily_cases2 = [int(x) if x != 'nan' else 0 for x in daily_cases]

            fig.add_trace(go.Scatter(x=country_daily_deaths_summary['Date'], y=daily_cases2, name=country, mode='lines'))

        fig.update_layout(
            template='plotly_dark',
            height=550,
            width=1200,
            title={
                'text': '<b>' + 'DAILY DEATHS - ' + month + ' ' + chosen_year + '</b>',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B')),
            yaxis=dict(title='<b>Deaths</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD')),
            #         legend=dict(x=0.07, y=0.98,traceorder="normal",bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
            xaxis_tickangle=90, )
        # fig.show()

        num_of_plots = len(chosen_countries)
        num_of_columns = 3
        num_of_rows = (num_of_plots // num_of_columns) + 1
        fig2_covid_death = make_subplots(rows=num_of_rows, cols=3,
                                         shared_xaxes=False,
                                         shared_yaxes=False,
                                         # vertical_spacing=0.5,
                                         vertical_spacing=0.6 / num_of_rows,
                                         # horizontal_spacing=0.03,
                                         subplot_titles=['title' for x in range(len(chosen_countries))],
                                         print_grid=False, )
        for country in country_daily_deaths_summary2.columns[1:]:
            # country_all_deaths = covid_deaths.loc[covid_deaths['Country_Other'] == country]
            daily_deaths = [0 if x == np.nan else str(x).replace('+', '').replace(',', '').replace('.0', '') for x in country_daily_deaths_summary2[country].values]
            daily_deaths2 = [int(x) if x != 'nan' else 0 for x in daily_deaths]
            country_index_position = chosen_countries.index(country)
            row = ((country_index_position // 3) + 1)
            col = ((country_index_position % 3) + 1)
            fig2_covid_death.add_trace(go.Scatter(x=country_daily_deaths_summary2['Date'], y=daily_deaths2, name=country, mode='lines',), row, col)
            fig2_covid_death.layout.annotations[chosen_countries.index(country)]['text'] = country
            fig2_covid_death.update_xaxes(tickangle=90, nticks=10,tickfont = dict(color='#9c9898'))

        fig2_covid_death.update_layout(
            template='plotly_dark',
            autosize=True,
            showlegend=False,
            margin=dict(l=80, r=80, t=100, b=80),
            height=1500,
            width=1200,
            title={
                'text': '<b>' + 'COVID19 DEATHS - ' + month + ' ' + chosen_year + '</b>',
                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},

                # yaxis=dict(title='<b>Deaths</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD')),
                # #         legend=dict(x=0.07, y=0.98,traceorder="normal",bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
             )
        table_header = 'COVID19 DEATHS - ' + month + ' ' + chosen_year
        return fig, fig2_covid_death, table_header,  dt.DataTable(data=data,
                                 id='dt_datatable',
                                 column_selectable= 'multi',
                                 # selected_rows=[],
                                 columns=columns,
                                 selected_columns=selected_countries,
                                 style_cell={'textAlign': 'left',
                                             'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'fontWeight': 'bold',
                                             'backgroundColor': 'rgb(22, 26, 29)',
                                             'width': 'auto',
                                             'color': '#fffafa'
                                             },
                                 style_header={
                                     'backgroundColor': 'forestGreen',
                                     'fontWeight': 'bold',
                                     'color': '#fdfdfd'
                                 },
                                 style_data_conditional=[
                                     {
                                         'if': {'row_index': 'odd'},
                                         'backgroundColor': '#232b2b'
                                     }
                                 ],
                                 ),
    else:
        return dash.no_update

@app.callback(
    Output('display_country_graph', 'figure'),
    Output('dt_datatable', 'style_data_conditional'),
    Input('dt_datatable', 'selected_columns'),
    State('select_countries', 'value'),
 )
def highlight_selected(selected_columns, selected_countries):
    if len(selected_countries) == 0:
        selected_columns = []
        # print(selected_columns)
        return genarate_new_country_graph([]), [{'if': {'column_id': i}, 'background_color': '#000080'} for i in selected_columns]

        # raise dash.exceptions.PreventUpdate
    elif len(selected_countries) == 1:
        # print(selected_columns)
        return genarate_new_country_graph(selected_columns), [{'if': {'column_id': i}, 'background_color': '#000080'} for i in selected_columns]

    elif len(selected_countries) >= 2:
        # print(selected_columns)
        return genarate_new_country_graph(selected_columns), [{'if': {'column_id': i}, 'background_color': '#000080'} for i in selected_columns]




