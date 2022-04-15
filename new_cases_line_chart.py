import dash
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import module


countries_new_cases = pd.read_csv('https://raw.githubusercontent.com/Ceenuggets/COVID19_Update/master/WorldNR/NewCases/NewCases.csv')
countries_new_recovered = pd.read_csv('https://raw.githubusercontent.com/Ceenuggets/COVID19_Update/master/WorldNR/NewRecovered/NewRecovered.csv')
countries_new_deaths = pd.read_csv('https://raw.githubusercontent.com/Ceenuggets/COVID19_Update/master/WorldNR/NewDeaths/NewDeaths.csv')

new_cases = [countries_new_cases, countries_new_recovered, countries_new_deaths]
case_description = ['New cases', 'New Recovery', 'New Deaths']
colors = ['teal', '#f0a150', 'crimson']
# dates = countries_new_cases.columns.to_list()
# dates = dates[1:]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dcc.Dropdown(id='countries_new_cases_graph_names',
                 options=module.sort_names(countries_new_cases),
                 value="South Africa",),
    html.Div(id='output_string'),

    dcc.Graph('coutput_graph')
    ])
@app.callback(
    # Output('output_string', 'children'),
    Output('coutput_graph', 'figure'),
    [Input('countries_new_cases_graph_names', 'value')]
)
def group_daily_cases(name):
    fig = go.Figure()
    for (i, case) in enumerate(new_cases, start=0):
        daily_cases = module.get_cases(case, name)
        fig.add_trace(go.Bar(x=module.format_date(module.get_dates(case)[-10:]), y=daily_cases[-10:],text=daily_cases[-10:],
                             textposition='outside', name= case_description[i], marker=dict(color=colors[i])))

        fig.update_layout(barmode='group',
                           height=550,
                           title={
                               'text': name.upper() + "- COVID19 NEW CASES, RECOVERIES AND DEATHS",
                               'y': 0.9,
                               'x': 0.5,
                               'xanchor': 'center',
                               'yanchor': 'top'},
                           xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD'),
                                      nticks=15),
                           yaxis=dict(title='<b>Cases</b>', titlefont_size=18),
                           xaxis_tickangle=90),

    return fig



    # for case in daily_cases:
    #     print(case)

if __name__ == '__main__':
    app.run_server(debug=True)


# print(dates)


# import time
# t0 = time.time()
#
# NRcountry_new_cases = countries_new_case[countries_new_case['Country_Other'] == 'South Africa']
# country_total_per_day = []
# for date in dates:
#     total = NRcountry_new_cases[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(0).astype(int)
#     country_total_per_day.append(int(total))
#
# # print(country_total_per_day)
#
# t1 = time.time()
# time_diff = t1-t0
# print(time_diff)
#
# import time
# t0 = time.time()
# NRcountry_new_cases = countries_new_case[countries_new_case['Country_Other'] == 'South Africa']
# NRcountry_new_cases = NRcountry_new_cases.copy()
# NRcountry_new_cases.fillna(0, inplace=True)
# NRcountry_new_cases = NRcountry_new_cases.replace("[+,]", "", regex=True)
# total_new_cases_per_day = []
# for date in dates:
#     total = NRcountry_new_cases[date]
#     total_new_cases_per_day.append(int(total))
# # NRcountry_new_cases.fillna(0, inplace=True)
# # NRcountry_new_cases = NRcountry_new_cases.apply(lambda x : NRcountry_new_cases.replace('+', '', regex=False))
# t1 = time.time()
# time_diff = t1-t0
# print(time_diff)
# # print(total_new_cases_per_day)
#
