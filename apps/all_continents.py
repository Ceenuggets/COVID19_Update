from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import  Input, Output
from app import app
import pathlib
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import dash_table as dt

import pandas as pd
import numpy as np
import datetime
from dash import dash_table


continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
cases = ['Total_Cases', 'New_Cases', 'Total_Deaths', 'New_Deaths', 'Total_Recovered', 'Active_Cases']
countries_and_continents = pd.read_csv('./GeneralFiles/CountriesAndContinents.csv', encoding='latin-1')

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../World/WorldSummary/Europe/").resolve()
CONTINENTS_DATA_PATH = PATH.joinpath("../World/WorldSummary/").resolve()
VIDEO_PATH = PATH.joinpath("../assets/").resolve()
vid_path = VIDEO_PATH.joinpath("COVID19ChartRace.mp4")
# print(vid_path)
# print(CONTINENTS_DATA_PATH)
# given_date = pd.read_csv('../World/WorldSummary/Europe/Europe_summary.csv').iloc[-1]['Date']
given_date = pd.read_csv(DATA_PATH.joinpath('Europe_summary.csv')).iloc[-1]['Date']
# print(given_date)

if '_' in given_date:
    given_date = datetime.datetime.strptime(given_date[:-7], '%b').strftime("%B") + ' ' + given_date[
                                                                                          -7:-5] + ', ' + given_date[
                                                                                                          -4:]
else:
    given_date = given_date[:-2] + ' ' + given_date[-2:] + ', ' + str(2020)


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') +'-' + x[-7:-5]+'-'+x[-4:] if '_'in x  else  datetime.datetime.strptime(x[:-2], "%B").strftime('%b') +'-' +x[-2:]+'-' +'2020'  for x in list_date]
    return x_date_format


#  GET RIGHT CSV FILE NAME FORMAT
date_val = datetime.datetime.strptime(given_date, "%B %d, %Y")
date_val = date_val.strftime('%d')+date_val.strftime('%m')+date_val.strftime('%Y')

# print(date_val)


def continent_new_cases_plot(all_continents):
    fig = go.Figure()
    for continent in all_continents:
        continent_mod = continent.replace(" ", "")
        # full_path = path + continent_mod + '/' + continent_mod + '_summary.csv'
        full_path = CONTINENTS_DATA_PATH.joinpath(continent_mod + '/' + continent_mod + '_summary.csv')
        summary = pd.read_csv(full_path)
        list_date = summary['Date'].tolist()
        fig.add_trace(go.Scatter(
            x=format_date(summary['Date'].tolist()),
            y=summary['Total_Cases'].tolist(),
            name=continent,
            mode='lines',
            line=dict(width=3)
        ))
    fig.update_layout(
        template='plotly_dark',
        height=550,
        # width=990, height=600, autosize=False,
        title={
            'text': '<b>' + 'COVID19 CONFIRMED CASES BY CONTINENT: ' + given_date + '</b>',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#4D4B4B'), nticks=15),
        yaxis=dict(title='<b>Confirmed Cases</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD')),
        legend=dict(x=0.07, y=0.98, traceorder="normal", bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)', ),
        xaxis_tickangle=90
    )
    return fig


def world_pie_chart(cases):
    fig = make_subplots(rows=3, cols=2,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}],
                               [{'type': 'domain'}, {'type': 'domain'}]], print_grid=False, vertical_spacing=0.005,
                        horizontal_spacing=0.085)

    case_val = []
    slice_colors = ['gold', '#007FFF', 'green', 'saddlebrown', 'cyan', 'crimson']
    position = 0
    x = [0.168, 0.82, 0.168, 0.82, 0.148, 0.82]
    y = [0.84, 0.84, 0.5, 0.5, 0.155, 0.155]
    for case in cases:
        row = ((position // 2) + 1)
        col = ((position % 2) + 1)
        for continent in continents:
            continent_mod = continent.replace(" ", "")
            # full_path = path + continent_mod + '\\' + continent_mod + '_summary.csv'
            full_path = CONTINENTS_DATA_PATH.joinpath(continent_mod + '/' + continent_mod + '_summary.csv')
            summary = pd.read_csv(full_path)
            case_val.append(summary.iloc[-1][case])
            case_mod = case.replace('_', '\n')

        fig.add_trace(go.Pie(labels=continents, values=case_val, name=case, customdata=['case']), row, col)
        fig.update_traces(hole=.35, hoverinfo="label+percent+name+value", textinfo='percent+value', textfont_size=14,
                          marker_colors=slice_colors, )
        case_val = []
        fig['layout']['annotations'] += tuple([dict(x=x[position], y=y[position], text='<b>' + case_mod + '</b>',
                                                    showarrow=False, font_size=12, font=dict(color='ghostwhite'))])
        fig.update_layout(
            template='plotly_dark',
            width=950, height=1450, autosize=False,
            title={'text': '<b>' + 'WORLD - COVID19 SUMMARY BY CONTINENT: ' + given_date + '</b>',
                   'y': 0.95,
                   'x': 0.46,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font_color': 'white',
                   'font_size': 18},
            legend=dict(x=1, y=1, traceorder="normal", font=dict(size=13))
        )
        position = position + 1
    return fig


# COUNTRIES WITH NO CASE IN THE LAST 30 DAYS
last_new_case_record = pd.read_csv('./World/LastNewCaseReport/LastNewCaseReport.csv', dtype=object, encoding='utf-8')
last_new_case_record['last_case'] = last_new_case_record['Last_New_Case_Report_Date']
last_new_case_record['last_case'] = pd.to_datetime(last_new_case_record['last_case'])

date_string = datetime.datetime.strptime(date_val, '%d%m%Y')


last_new_case_record['number_of_days'] =  date_string - last_new_case_record['last_case']


last_new_case_record['days'] = last_new_case_record['number_of_days'].apply(lambda x : str(x).split(' ')[0])

last_new_case_record['days'] = last_new_case_record['days'].astype(int)
# last_new_case_record['days']
last_new_case_record.sort_values(by='days', ascending=True, inplace=True)
upto_a_month_free = last_new_case_record[last_new_case_record['days'] >= 30]
upto_a_month_free = upto_a_month_free.copy()
upto_a_month_free['last_case_num_of_days'] = upto_a_month_free['days'].apply(lambda x : (str(x)+" days"))
# upto_a_month_free = upto_a_month_free.copy()
diamond_princes = upto_a_month_free.index[upto_a_month_free['Country_Other'] == 'Diamond Princess'][0]
ms_zaandam = upto_a_month_free.index[upto_a_month_free['Country_Other'] == 'MS Zaandam'][0]
upto_a_month_free.drop(['New_Cases','last_case','number_of_days','days'], axis=1, inplace=True)
upto_a_month_free.drop([diamond_princes, ms_zaandam],  inplace=True)
upto_a_month_free.reset_index(drop=True, inplace=True)
upto_a_month_free.rename(columns={'Country_Other' : 'Country_Other', 'Total_Cases' : 'Total Cases', 'Total_Recovered' : 'Total Recovered', 'Total_Deaths' : 'Total Deaths', 'Active_Cases' : 'Active Cases',
                                  'Last_New_Case_Report_Date' : 'Last Case Date',  'last_case_num_of_days' : 'Days Since Last Case'}, inplace=True )
col_index = 0
new_col_name = [i for i in range(1,len(upto_a_month_free)+1)]
upto_a_month_free.insert(loc=col_index, column='S/N', value=new_col_name)
# [print(i) for i in upto_a_month_free.columns]

# print(upto_a_month_free.columns)

layout = html.Div(children=[
       # html.H1("Hello dears"),
    dbc.Row(
        [
            dbc.Col(dcc.Graph('continent_graph', figure=continent_new_cases_plot(continents)),
                    xs=11, sm=11, md=11, lg=6, xl=6),
            dbc.Col(html.Video(controls = True, id='movie_player', src="../assets/COVID19ChartRace.mp4", autoPlay=True, loop=True,width='100%', height='100%'),
                    xs=11, sm=11, md=11, lg=6, xl=6)
        ]
    ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(dcc.Graph('continent_pie_chart', figure=world_pie_chart(cases)), width={'size': 10}),
            dbc.Col(
                [
                    html.Label(id='table_caption', style={'color': '#FFFFFF','fontSize': '20px','textAlign':'center','fontWeight': 'bold','marginTop': '280px', }),
                    html.Label(id='user_guide_general_pie_chart', style={'color': '#00FFFF','fontSize': '11px','textAlign':'center','fontWeight': 'bold', 'margin': '0px', 'padding': '0px', 'fontFamily': 'calibri,Times New Roman, san-serif'}),
                    html.Div(id='pie_hover_result', style={'marginLeft': '3px'}),
                ], width={'size': 2}
            ),
        ]
    ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col([
                # html.Div('Data table pagination test'),
                html.Div([
                          html.Div(html.Label('No new case in the past thirty-plus consecutive days', style={'color': '#00FFFF','fontSize': '24px', 'fontWeight': 'bold', 'margin': '0px', 'textAlign':'justify'}), ),
                          dash_table.DataTable(
                              id='last_new_case_datatable',
                              columns=[{"name": i, "id": i} for i in upto_a_month_free.columns],
                              data=upto_a_month_free.to_dict('records'),
                              # style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95},
                              # style_data=dict(color="white"),
                              page_current=0,
                              page_size=20,
                              style_cell_conditional=[
                                  {
                                      'if': {'column_id': i},
                                      'textAlign': 'left'
                                  } for i in ['Country_Other', 'Last Case Date', 'Days Since Last Case']
                              ],
                              # style_as_list_view=True,
                              style_header={
                                  'backgroundColor': '#000133',
                                  'fontWeight': 'bold',
                                  'color': 'white',
                              },
                              fill_width=False,
                              style_cell={
                                  'whiteSpace': 'normal',
                                  'height': 'auto',
                                  'fontWeight': 'bold',
                                  'backgroundColor': '#041E42',
                                  'width': 'auto',
                              },
                              # style_table={
                              #  'width': '50%',
                              #     'minWidth': '50%',
                              #     'backgroundColor': '#282828'
                              #     # 'fontFamily': 'Times New Roman'
                              # },
                              page_action="native",

                          ),
                          ], style={'width': '100%',}),
            ], width={'size': 10, 'offset': 2})
        ]
    ),
#     Next row/graph here

])


@app.callback(
    Output('table_caption', 'children'),
    Output('user_guide_general_pie_chart', 'children'),
    Output('pie_hover_result', 'children'),
    Input('continent_pie_chart', 'hoverData'),
    Input('continent_pie_chart', 'clickData')
)
def display_pie_chart_hover_data(hov_data, clk_data):
    common_path = './World/'
    user_guide = '(Click on the pie chart for more updates)'
    slice_colors = {'Africa': 'gold', 'Asia': '#007FFF', 'Europe': 'green', 'North America': 'saddlebrown','Oceania': 'cyan', 'South America': 'crimson'}
    ##### # 0f52ba(Azure blue)
    caption = ''
    if clk_data is None:
        table_data = pd.read_csv('./World/NewCases/DailyCases'+date_val+'.csv')
        country_region = countries_and_continents[countries_and_continents['continent'] == 'Europe']
        current_case = table_data[table_data['Country_Other'].isin(country_region['country_Other'])]
        current_case = current_case.copy()
        current_case.fillna(0, inplace=True)
        current_case.reset_index(drop=True)
        current_case_sorted = current_case.iloc[:, [0] + [-1]]
        last_column_name = current_case_sorted[current_case_sorted.columns[-1]].name
        last_column_date =''
        if '_' in last_column_name:
            last_column_date = datetime.datetime.strptime(last_column_name[:-7], '%b').strftime("%B") + ' ' + last_column_name[-7:-5] + ', ' + last_column_name[-4:]
        current_case_sorted = current_case_sorted.copy()
        current_case_sorted['column_sort'] = current_case_sorted[last_column_name].apply(lambda x: str(x).replace('+', '').replace(',', ''))
        current_case_sorted['column_sort'] = pd.to_numeric(current_case_sorted['column_sort'])
        current_case_sorted.sort_values(by=['column_sort'], ascending=False, inplace=True)
        current_case_sorted.drop(['column_sort'], axis=1, inplace=True)
        current_case_sorted = current_case_sorted.rename(columns={'Country_Other': 'Europe', last_column_name: 'New Cases'})
        data = current_case_sorted.to_dict('records')
        columns = [{"name": i, "id": i, } for i in current_case_sorted.columns]
        caption = 'Europe', html.Br(), last_column_date
        # print(current_case_sorted)
        return caption, user_guide, dt.DataTable(data=data,
                                     columns=columns,
                                     page_size=30,
                                     style_table={
                                             'width': '100%',
                                             'minWidth': '100%',
                                             'margin': '0 auto',
                                             # 'backgroundColor': '#282828'
                                         # 'fontFamily': 'Times New Roman'
                                     },
                                     style_cell={'textAlign': 'left',
                                                 'whiteSpace': 'normal',
                                                 'height': 'auto',
                                                 'fontWeight': 'bold',
                                                 'backgroundColor': 'rgb(22, 26, 29)',
                                                 'width': 'auto',
                                                 'color': '#fffafa'},
                                     style_header={
                                         'whiteSpace': 'nowrap',
                                         'backgroundColor': 'green',
                                         'color': '#fdfdfd'},
                                     style_data_conditional=[
                                         {
                                             'if': {'row_index': 'odd'},
                                             'backgroundColor': '#232b2b'
                                         }
                                     ],
                                     ),

    else:
        curve_number = clk_data['points'][0]['curveNumber']
        trace_name = layout['continent_pie_chart'].figure['data'][curve_number]['name']
        # #######Use code below if your application has app.layout()
        # #######trace_name = app.layout['continent_pie_chart'].figure['data'][curve_number]['name']
        clk_data['points'][0]['curveNumber'] = trace_name
        # print(f'Hover Data: {hov_data}')
        country_location = clk_data['points'][0]['label']

        data_name = clk_data['points'][0]['curveNumber']
        # print(f'Hover Data: {country_location} {data_name}')
        caption_info = data_name.replace("_", " ")

        # print(caption)
        path_info = data_name.replace("_", "")
        if path_info == 'NewCases':
            table_data = pd.read_csv(common_path + path_info + '/' + 'DailyCases' + date_val + '.csv')
        else:
            table_data = pd.read_csv(common_path + path_info + '/' + path_info + date_val + '.csv')

        country_region = countries_and_continents[countries_and_continents['continent'] == country_location]
        current_case = table_data[table_data['Country_Other'].isin(country_region['country_Other'])]
        current_case = current_case.copy()
        current_case.fillna(0, inplace=True)
        current_case.reset_index(drop=True)
        current_case_sorted = current_case.iloc[:, [0] + [-1]]
        last_column_name = current_case_sorted[current_case_sorted.columns[-1]].name
        last_column_date = ''
        if '_' in last_column_name:
            last_column_date = datetime.datetime.strptime(last_column_name[:-7], '%b').strftime(
                "%B") + ' ' + last_column_name[-7:-5] + ', ' + last_column_name[-4:]
        current_case_sorted = current_case_sorted.copy()
        current_case_sorted['column_sort'] = current_case_sorted[last_column_name].apply(lambda x: str(x).replace('+', '').replace(',', ''))
        current_case_sorted['column_sort'] = pd.to_numeric(current_case_sorted['column_sort'])
        current_case_sorted.sort_values(by=['column_sort'], ascending=False, inplace=True)
        current_case_sorted.drop(['column_sort'], axis=1, inplace=True)
        caption = country_location, html.Br(), last_column_date
        current_case_sorted = current_case_sorted.rename(columns={'Country_Other': country_location, last_column_name: caption_info})
        data = current_case_sorted.to_dict('records')
        columns = [{"name": i, "id": i, } for i in current_case_sorted.columns]
        # print(caption)

        return caption, user_guide, dt.DataTable(data=data,
                                     columns=columns,
                                     page_size=30,
                                     style_cell={'textAlign': 'left',
                                                 'whiteSpace': 'normal',
                                                 'height': 'auto',
                                                 'fontWeight': 'bold',
                                                 'backgroundColor': 'rgb(22, 26, 29)',
                                                 'width': 'auto',
                                                 'color': '#fffafa'},
                                     style_header={
                                         'whiteSpace': 'nowrap',
                                         'backgroundColor': slice_colors[country_location.strip()],
                                         'fontWeight': 'bold',
                                         'color': '#fdfdfd'},
                                     style_data_conditional=[
                                         {
                                             'if': {'row_index': 'odd'},
                                             'backgroundColor': '#232b2b'
                                         }
                                     ],
                                     ),



