# from dash import dcc
# from dash import
from dash import dcc, Input, Output, callback, State, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import datetime

import plotly.graph_objs as go
from plotly.subplots import make_subplots


given_date = pd.read_csv('./World/WorldSummary/Europe/Europe_summary.csv').iloc[-1]['Date']


if '_' in given_date:
    given_date = datetime.datetime.strptime(given_date[:-7], '%b').strftime("%B") + ' ' + given_date[
                                                                                          -7:-5] + ', ' + given_date[
                                                                                                          -4:]
else:
    given_date = given_date[:-2] + ' ' + given_date[-2:] + ', ' + str(2020)


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') +'-' + x[-7:-5]+'-'+x[-4:] if '_'in x  else  datetime.datetime.strptime(x[:-2], "%B").strftime('%b') +'-' +x[-2:]+'-' +'2020'  for x in list_date]
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


#  GET RIGHT CSV FILE NAME FORMAT
date_val = datetime.datetime.strptime(given_date, "%B %d, %Y")
date_val = date_val.strftime('%d')+date_val.strftime('%m')+date_val.strftime('%Y')
date_file ="DailyCases"+str(date_val)+".csv"

countries_new_cases  = pd.read_csv('./World/NewCases/' + date_file)

dates = countries_new_cases.columns.to_list()
dates = dates[1:]

# countries_and_continents = pd.read_csv('./GeneralFiles/CountriesAndContinents.csv')

countries_and_continents = pd.read_csv('./GeneralFiles/CountriesAndContinents.csv', encoding='latin-1')
continents = countries_and_continents['continent'].sort_values(ascending=True).unique().tolist()
continents.remove('Other')

countries_new_cases_sorted = countries_new_cases.iloc[:, [0] + list(range(-6, 0))]

region_value_Bar_dict = {}

def select_color(continent):
    Europe = ['#33A9AC', '#18C729', '#EF3D59', '#F7DC68']
    Asia =  ['#4F48EC', '#F46C3F',  '#00BE65','#1CB1DC', '#FBD095']
    Africa = ['crimson', 'green', 'saddlebrown', 'yellow', 'blue']
    North_America = ['green', '#40CEE3', '#42A5F5']
    Oceania = ['#4F48EC', '#2ECC71', '#9B59B6', '#17E9E1']
    South_America = ['#E17A47']
    if continent == "Europe":
        return Europe
    elif continent == "Asia":
        return Asia
    elif continent == "Africa":
        return Africa
    elif continent == "North America":
        return North_America
    elif continent == "Oceania":
        return Oceania
    elif continent == "South America":
        return South_America
    else:
        return Africa


def select_color2(continent):
    Europe = ['#33A9AC', '#18C729', '#EF3D59', '#F7DC68']
    Asia =  ['#4F48EC', '#F46C3F',  '#00BE65','#1CB1DC', '#FBD095']
    Africa = ['crimson', 'green', 'saddlebrown', 'yellow', 'blue']
    North_America = ['green', '#40CEE3', '#42A5F5']
    Oceania = ['#4F48EC', '#2ECC71', '#9B59B6', '#17E9E1']
    South_America = ['#E17A47']
    if continent == "Europe":
        return Europe[::-1]
    elif continent == "Asia":
        return Asia[::-1]
    elif continent == "Africa":
        return Africa[::-1]
    elif continent == "North America":
        return North_America[::-1]
    elif continent == "Oceania":
        return Oceania[::-1]
    elif continent == "South America":
        return South_America[::-1]
    else:
        return Africa[::-1]


layout = html.Div(children=[
    dbc.Row([
        dbc.Col(
        [
            html.Label('Select Continent:', style={'paddingTop': '.3rem'}),
            dcc.Dropdown(
                id="continents_by_name",
                options=[{'label': i, 'value': i} for i in
                         countries_and_continents['continent'].sort_values(ascending=True).unique() if i != 'Other'],
                searchable=False,
                clearable=False,
                value="Europe",
                style={'fontSize': '18px', 'fontWeight': 'bold',}
             ),
        ], xs=11, sm=11, md=11, lg=3, xl=3)

    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph('continent_pie_chart'),  xs=8, sm=8, md=8, lg=8, xl=8),
        dbc.Col(dcc.Graph('continent_bar_chart'), xs=6, sm=6, md=6, lg=4, xl=4),
        ],
        no_gutters=True,
    ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                html.Div(html.Img(src='/assets/africa_first_10.PNG', style={'width': '100%', 'height': '100%'}),
                         style={'width': '100%', }),

                # width={'size': 10, 'offset': 1}
                width={'size': 10}
            )
        ]
    ),
    html.Br(),

    dbc.Row(
        [
            dbc.Col(html.Img(src='/assets/first_twenty.PNG', style={'width': '100%', 'height': '100%'}),
                    # width={'size': 10, 'offset': 1}
                    width={'size': 10}
                    )
        ]
    ),
])


@callback(Output('continent_pie_chart', 'figure'),
          Input('continents_by_name', 'value'),)
def display_result(continent):
    status = 0
    fig = make_subplots(rows=3, cols=2,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}],
                               [{'type': 'domain'}, {'type': 'domain'}]], print_grid=False, vertical_spacing=0.005,
                        horizontal_spacing=0.100)

    # x = [0.168, 0.83, 0.168, 0.83, 0.168, 0.83]
    # y = [0.84, 0.84, 0.5, 0.5, 0.155, 0.155]

    x = [0.152, 0.85, 0.152, 0.85, 0.152, 0.85]
    y = [0.84, 0.84, 0.5, 0.5, 0.155, 0.155]


    slice_colors = ['crimson', 'green', 'saddlebrown', 'yellow', 'blue']

    first_plot_date = countries_new_cases_sorted[countries_new_cases_sorted.columns[1]].name
    last_plot_date =countries_new_cases_sorted[countries_new_cases_sorted.columns[-1]].name
    countries_of_continents = countries_and_continents[countries_and_continents['continent'] == continent]
    country_regions = list(countries_of_continents['region'].unique())
    position = 0
    select_region_Bar = []
    select_region_stat_Bar =[]
    column_Bar = ""

    region_value_Bar_dict_sorted ={}

    for column in countries_new_cases_sorted.columns[1:][::-1]:
        select_region = []
        select_region_stat = []
        row = ((position // 2) + 1)
        col = ((position % 2) + 1)
        # print(column)
        for region in country_regions:
            dynamic_region_name = region.replace(" ", "_")
            dynamic_region_name = countries_and_continents[
                (countries_and_continents['continent'] == continent) & (countries_and_continents['region'] == region)]
            dynamic_region_name_new_cases = countries_new_cases[
                countries_new_cases['Country_Other'].isin(dynamic_region_name['country_Other'])]
            dynamic_region_name_new_cases = dynamic_region_name_new_cases.iloc[:, [0] + list(range(-6, 0))]
            dynamic_region_name_new_cases.fillna(0, inplace=True)
            dynamic_region_name_new_cases.reset_index(drop=True)

            region_total = countries_new_cases[
                countries_new_cases['Country_Other'].isin(dynamic_region_name_new_cases['Country_Other'])]
            region_total = region_total.copy()
            region_total.fillna(0, inplace=True)
            region_sum = region_total[column].astype(str).str.replace('+', '', regex=False).fillna(
                0).str.replace(',', '', regex=False).fillna(0).astype(int).sum()
            select_region.append(region)
            select_region_stat.append(region_sum)

            if column == last_plot_date:
                select_region_Bar.append(region)
                select_region_stat_Bar.append(region_sum)
                column_Bar = column
                region_value_Bar_dict[region] = region_sum
            region_value_Bar_dict_sorted = dict(sorted(region_value_Bar_dict.items(), key=lambda kv: kv[1], reverse=True))

        fig.add_trace(go.Pie(labels=select_region, values=select_region_stat, name=column,  customdata=[column]), row, col)
        fig.update_traces(hole=.4, hoverinfo="label+percent+name+value", textinfo='percent+value',
                              textfont_size=13, marker_colors=select_color(continent), )
        fig['layout']['annotations'] += tuple([dict(x=x[position], y=y[position],
                                                    text='<b>' + pie_date_format(column) + '</b>', showarrow=False,
                                                    font_size=12, font=dict(color='black'))])
        fig.update_layout(
            width=820, height=1100, autosize=False,
            title={'text': '<b>' + continent.upper() + ' - COVID19 NEW CASES : ' + pie_date_format(first_plot_date) + ' to ' + pie_date_format(last_plot_date) + '</b>',
                   'y': 0.95,
                   'x': 0.46,
                   # "yref": "container",
                   'xanchor': 'center',
                   'yanchor': 'bottom',
                   'font_color': 'black',
                   'font_size': 18,},
            legend=dict(x=1, y=1, traceorder="normal", font=dict(size=13))
        )
        position = position + 1

    return fig


@callback(
    Output("continent_bar_chart", "figure"),
    [Input('continent_pie_chart', 'clickData'),
     State('continent_pie_chart', 'figure'),
     Input('continents_by_name', 'value')]
)
def display_bar_chart(clickData, figure, continent):
    all_continents = {"Africa" : ["Central Africa", "East Africa", "North Africa", "South Africa", "West Africa"],
                      "Asia" : ["Central Asia", "East Asia", "South Asia", "SouthEast Asia", "Western Asia"],
                      "Europe" : ["Eastern Europe", "Northern Europe", "Southern Europe", "Western Europe"],
                      "North_America": ["Caribbean", "Central America", "Northern America"],
                      "Oceania": ["Oceania", "Oceania-Melanesia", "Oceania-Micronesia", "Oceania-Polynesia"],
                      "South_America" : ["South America"]}

    dropdown_changed = False

    if clickData is not None:
        clicked_slice_name = clickData['points'][0]['label']
        for key, value in all_continents.items():
            key = key.replace("_", " ")
            if key == continent:
                if clicked_slice_name in value:
                    dropdown_changed = True
                    # print(key)
                    # print(clicked_slice_name)
                else:
                    dropdown_changed = False

        if dropdown_changed is True:
            fig = go.Figure()
            slice_name = clickData['points'][0]['label']
            slice_color = clickData['points'][0]['color']
            curve_number = clickData['points'][0]['curveNumber']
            slice_value = clickData['points'][0]['value']
            trace_name = figure['data'][curve_number]['name']
            modal_title = slice_name + ' New Cases - ' + given_date,
            select_region_countries = list(
                countries_and_continents[countries_and_continents['region'] == slice_name]['country_Other'])
            region_countries_new_cases = countries_new_cases[
                countries_new_cases['Country_Other'].isin(select_region_countries)]
            df_trace_name_countries = region_countries_new_cases[['Country_Other', trace_name]]
            df_trace_name_countries = df_trace_name_countries.copy()
            df_trace_name_countries.dropna(axis=0, inplace=True)
            df_trace_name_countries[trace_name] = df_trace_name_countries[trace_name].apply(
                lambda x: x.replace('+', '').replace(',', '').replace('.0', ''))
            df_trace_name_countries[trace_name] = pd.to_numeric(df_trace_name_countries[trace_name])
            df_trace_name_countries.sort_values(by=[trace_name], ascending=True, inplace=True)
            country_values = [int(i) for i in df_trace_name_countries[trace_name].tolist()]
            fig.add_trace(
                go.Bar(x=country_values, y=df_trace_name_countries['Country_Other'].tolist(),
                       text=df_trace_name_countries[trace_name].tolist(),
                       textposition='inside',
                       name="New Cases",
                       orientation='h',
                       marker=dict(color=slice_color, )))

            fig.update_layout(
                height=550,
                width=400,
                title={'text': '<b>' + slice_name + ' - COVID19 New Cases: ' + pie_date_format(trace_name) + '</b>',
                       'y': 0.95,
                       'x': 0.46,
                       'xanchor': 'center',
                       'yanchor': 'top',
                       'font_color': 'cyan',
                       'font_size': 12,},
                template='plotly_dark',
                xaxis=dict(title='<b>New Cases</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
                # yaxis=dict(title='<b>Date</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
                yaxis_tickangle=45,
            )

            return fig
        else:
            fig1 = go.Figure()
            last_plot_date = countries_new_cases_sorted[countries_new_cases_sorted.columns[-1]].name
            countries_of_continents = countries_and_continents[countries_and_continents['continent'] == continent]
            country_regions = list(countries_of_continents['region'].unique())
            region_value_Bar_dict_sorted = {}
            select_region = []
            select_region_stat = []
            region_value_Bar_dict = {}
            for region in country_regions:
                dynamic_region_name = region.replace(" ", "_")
                dynamic_region_name = countries_and_continents[
                    (countries_and_continents['continent'] == continent) & (
                                countries_and_continents['region'] == region)]
                dynamic_region_name_new_cases = countries_new_cases[
                    countries_new_cases['Country_Other'].isin(dynamic_region_name['country_Other'])]
                dynamic_region_name_new_cases = dynamic_region_name_new_cases.iloc[:, [0] + list(range(-6, 0))]
                dynamic_region_name_new_cases.fillna(0, inplace=True)
                dynamic_region_name_new_cases.reset_index(drop=True)

                region_total = countries_new_cases[
                    countries_new_cases['Country_Other'].isin(dynamic_region_name_new_cases['Country_Other'])]
                region_total = region_total.copy()
                region_total.fillna(0, inplace=True)
                region_sum = region_total[last_plot_date].astype(str).str.replace('+', '', regex=False).fillna(
                    0).str.replace(',', '', regex=False).fillna(0).astype(int).sum()
                select_region.append(region)
                select_region_stat.append(region_sum)
                region_value_Bar_dict[region] = region_sum
            region_value_Bar_dict_sorted = dict(
                sorted(region_value_Bar_dict.items(), key=lambda kv: kv[1], reverse=True))
            sorted_key_Bar = [key for key, value in region_value_Bar_dict_sorted.items()]
            sorted_values_Bar = [value for key, value in region_value_Bar_dict_sorted.items()]
            fig1.add_trace(
                go.Bar(x=sorted_values_Bar[::-1], y=sorted_key_Bar[::-1],
                       text=sorted_values_Bar[::-1],
                       textposition='inside',
                       name="New Cases",
                       orientation='h',
                       # marker=dict(color=select_color2(continent), )
                       marker=dict(color='orange',)
                       ))

            fig1.update_layout(
                height=550,
                width=400,
                title={'text': '<b>' + continent + ' - COVID19 New Cases: ' + pie_date_format(last_plot_date) + '</b>',
                       'y': 0.95,
                       'x': 0.46,
                       'xanchor': 'center',
                       'yanchor': 'top',
                       'font_color': 'cyan',
                       'font_size': 12},
                template='plotly_dark',
                xaxis=dict(title='<b>New Cases</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
                # yaxis=dict(title='<b>Date</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
                yaxis_tickangle=45,
            )
            # fig1.show()
            # print(select_region)
            # print(select_region_stat)
            # print(region_value_Bar_dict_sorted)
            # raise dash.exceptions.PreventUpdate
            return fig1
    else:
        # print(figure)
        fig1 = go.Figure()
        last_plot_date = countries_new_cases_sorted[countries_new_cases_sorted.columns[-1]].name
        countries_of_continents = countries_and_continents[countries_and_continents['continent'] == continent]
        country_regions = list(countries_of_continents['region'].unique())
        region_value_Bar_dict_sorted = {}
        select_region = []
        select_region_stat = []
        region_value_Bar_dict = {}
        for region in country_regions:
            dynamic_region_name = region.replace(" ", "_")
            dynamic_region_name = countries_and_continents[
                (countries_and_continents['continent'] == continent) & (countries_and_continents['region'] == region)]
            dynamic_region_name_new_cases = countries_new_cases[countries_new_cases['Country_Other'].isin(dynamic_region_name['country_Other'])]
            # print(countries_new_cases)
            dynamic_region_name_new_cases = dynamic_region_name_new_cases.iloc[:, [0] + list(range(-6, 0))]
            dynamic_region_name_new_cases.fillna(0, inplace=True)
            dynamic_region_name_new_cases.reset_index(drop=True)

            region_total = countries_new_cases[
                countries_new_cases['Country_Other'].isin(dynamic_region_name_new_cases['Country_Other'])]
            region_total = region_total.copy()
            region_total.fillna(0, inplace=True)
            region_sum = region_total[last_plot_date].astype(str).str.replace('+', '', regex=False).fillna(
                0).str.replace(',', '', regex=False).fillna(0).astype(int).sum()
            select_region.append(region)
            select_region_stat.append(region_sum)
            region_value_Bar_dict[region] = region_sum
        region_value_Bar_dict_sorted = dict(sorted(region_value_Bar_dict.items(), key=lambda kv: kv[1], reverse=True))
        sorted_key_Bar = [key for key, value in region_value_Bar_dict_sorted.items()]
        sorted_values_Bar = [value for key, value in region_value_Bar_dict_sorted.items()]
        fig1.add_trace(
            go.Bar(x=sorted_values_Bar[::-1], y=sorted_key_Bar[::-1],
                   text=sorted_values_Bar[::-1],
                   textposition='inside',
                   name="New Cases",
                   orientation='h',
                   # marker=dict(color=select_color2(continent),)
                   marker=dict(color='orange', )
                   ))

        fig1.update_layout(
            height=550,
            width=400,
            title={'text': '<b>' + continent + ' - COVID19 New Cases: ' + pie_date_format(last_plot_date) + '</b>',
                   'y': 0.95,
                   'x': 0.46,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font_color': 'cyan',
                   'font_size': 12},
            template='plotly_dark',
            xaxis=dict(title='<b>New Cases</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
            # yaxis=dict(title='<b>Date</b>', titlefont_size=14, titlefont=dict(color='#BDBDBD')),
            yaxis_tickangle=45,
        )

        return fig1
