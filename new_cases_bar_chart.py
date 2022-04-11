import pandas as pd
import plotly.graph_objs as go
import datetime

countries_new_cases = pd.read_csv('https://raw.githubusercontent.com/Ceenuggets/COVID19_Update/master/World/NewCases/DailyCases.csv')
country_name = 'USA'
country = countries_new_cases[countries_new_cases['Country_Other'] == country_name]


def format_date(list_date):
    x_date_format = [datetime.datetime.strptime(x[:-7], "%b").strftime('%b') + '-' + x[-7:-5] + '-' + x[
                                                                                                      -4:] if '_' in x else datetime.datetime.strptime(
        x[:-2], "%B").strftime('%b') + '-' + x[-2:] + '-' + '2020' for x in list_date]
    return x_date_format


dates = countries_new_cases.columns.to_list()
dates = dates[1:]
country_total_per_day = []

fig = go.Figure()
for date in dates:
    total = country[date].str.replace('+', '', regex=False).str.replace(',', '', regex=False).fillna(0).astype(int)
    country_total_per_day.append(int(total))

fig.add_trace(go.Bar(x=format_date(dates[-20:]), y=country_total_per_day[-20:], text=country_total_per_day[-20:],
                     textposition='outside',name=country_name, marker=dict(color='#32cd32', )))
fig.update_layout(
        height=550,
        # template='plotly_dark',
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

fig.show()

