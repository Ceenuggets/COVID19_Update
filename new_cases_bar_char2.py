import dash
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import module


countries_new_cases = pd.read_csv('https://raw.githubusercontent.com/Ceenuggets/COVID19_Update/master/World/NewCases/DailyCases.csv')

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
def chosen_name(name):
    fig = go.Figure()
    daily_cases = module.get_cases(countries_new_cases, name)
    fig.add_trace(
        go.Bar(x=module.format_date(module.get_dates(countries_new_cases)[-20:]), y=daily_cases[-20:], text=daily_cases[-20:],
               textposition='outside', name=name, marker=dict(color='#32cd32', )))
    fig.update_layout(
        height=550,
        # template='plotly_dark',
        title={
            'text': name.upper() + "- COVID19 DAILY NEW CASES",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis=dict(title='<b>Date</b>', titlefont_size=18, titlefont=dict(color='#BDBDBD')),
        yaxis=dict(title='<b>New Cases</b>', titlefont_size=18),
        xaxis_tickangle=90,
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8116)

