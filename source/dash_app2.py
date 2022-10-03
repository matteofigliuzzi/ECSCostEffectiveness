# Run this app with `python dash_app_template.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import base64
import datetime
import io
from dash import dash_table, State
from dash import dependencies

import pandas as pd
from psa import Psa
# from cgt_data import *
from load_data import data_loader

app = Dash(__name__, suppress_callback_exceptions=True)

# disease_dict, strategy_dict = load_data()

file_disease = '../data/Dati Input Disease.xlsx'
file_strategies = '../data/Dati Input Strategies.xlsx'
file_costs = '../data/Dati Input Costs.xlsx'

data_loader = data_loader(file_disease,file_strategies,file_costs=file_costs)


# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app.layout = html.Div([

    html.Div([

        html.H2("1 - Upload Data"),

        html.Div([
            html.H3("Upload Disease Data"),

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select File')
                ]), style={
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ],style={
                    'width': '48%',
                    'display': 'inline-block'
                }),

        html.Div([
            html.H3("Upload Strategy Data"),

            dcc.Upload(
                id='upload-data-strategy',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select File')
                ]), style={
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload-strategy'),
        ], style={
                    'width': '48%',
                    'display': 'inline-block',
                    'float': 'right',
                }),

    ]),
    html.Br(),

    html.Div([
        html.H2("2 - Select strategies"),

        html.Div([


            html.H3("Strategy 1"),
            dcc.Dropdown(
                ['No testing'], #list(data_loader.strategy_dict.keys()),  # ['no testing', 'limited testing', 'full testing'],
                'No testing', #list(data_loader.strategy_dict.keys())[0],
                id='strategy1'
            ),
            html.Div(
                [
                    html.H6("Strategy 1 cost (Euros)"),
                    # dcc.Input(type='number', value=0),
                    dcc.RangeSlider(
                        id='strategy1_cost',
                        min=0,
                        max=1500,
                        value=[240, 240],
                        allowCross=False
                    ),
                    # dcc.Input(type='number', value=1)
                ])
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H3("Strategy 2"),
            dcc.Dropdown(
                ['No testing'],
                # list(data_loader.strategy_dict.keys()),  # ['no testing', 'limited testing', 'full testing'],
                'No testing',  # list(data_loader.strategy_dict.keys())[0],
                id='strategy2'
            ),
            html.Div(
                [
                    html.H6("Strategy 2 cost (Euros)"),
                    # dcc.Input(type='number', value=0),
                    dcc.RangeSlider(
                        id='strategy2_cost',
                        min=0,
                        max=1500,
                        value=[0, 0],
                        allowCross=False
                    ),
                    # dcc.Input(type='number', value=1)
                ])
            # dcc.RadioItems(
            #    ['Linear', 'Log'],
            #    'Linear',
            #    id='yaxis-type',
            #    inline=True
            # )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})

    ]),

    html.H2("3 - Tune parameters"),
    html.Div([
        html.H3("Intervention parameters"),
        html.Div(
            [
                html.H6("Intervention costs (Euros)"),
                # dcc.Input(type='number', value=0),
                dcc.RangeSlider(
                    id='intervention_cost',
                    min=0,
                    max=40000,
                    value=[19714, 19714],
                    allowCross=False
                ),
                # dcc.Input(type='number', value=1)
            ]),
        html.Div(
            [
                html.H6("Intervention Probability"),
                # dcc.Input(type='number', value=0),
                dcc.RangeSlider(
                    id='intervention_probability_bounds',
                    min=0,
                    max=1,
                    value=[0.77, 0.77],
                    allowCross=False
                ),
                # dcc.Input(type='number', value=1)
            ]
        )],
        style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H3("Testing errors"),
        html.Div(
            [
                html.H6("Carrier screening error (FN rate)"),
                # dcc.Input(type='number', value=0),
                dcc.RangeSlider(
                    id='eps_cs_bounds',
                    min=0,
                    max=0.1,
                    value=[0.0, 0.00],
                    allowCross=False
                ),
                # dcc.Input(type='number', value=1)
            ]),
        html.Div(
            [
                html.H6("Intervention error (FN rate)"),
                # dcc.Input(type='number', value=0),
                dcc.RangeSlider(
                    id='eps_pgt_bounds',
                    min=0,
                    max=0.1,
                    value=[0.0, 0.00],
                    allowCross=False
                ),
                # dcc.Input(type='number', value=1)
            ]
        )], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    # ,style={"display": "grid", "grid-template-columns": "10% 40% 10%"}

    html.Br(),
    html.H2('Deterministic results'),

    html.Div([
        html.H6("Total Cost strategy 1 (Euros)"),
        html.Div(id='out_total_cost1'),
        html.Div(id='in_total_cost1'),
        html.H6("Life expectancy strategy 2 (Years)"),
        html.Div(id='out_life_exp1'),
        html.Div(id='in_life_exp1'),
        # dcc.Input(type='number', value=1)
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H6("Total Cost strategy 2 (Euros)"),
        html.Div(id='out_total_cost2'),
        html.Div(id='in_total_cost2'),
        html.H6("Life expectancy strategy 2 (Years)"),
        html.Div(id='out_life_exp2'),
        html.Div(id='in_life_exp2'),
        # html.Div(id='my-output'),
        # dcc.Input(type='number', value=1)
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    html.Div([
        html.H6("ICER (Euros / LYG)"),
        html.Div(id='out_icer'),
        html.Div(id='in_icer'),
        html.Br(),
        html.Br(),
        html.Br(),

        # dcc.Input(type='number', value=1)
    ], style={'width': '32%', 'float': 'center', 'display': 'inline-block'}),

    html.H2('Probabilistic results'),
    html.Br(),
    html.H3('CEAC graph'),
    dcc.Graph(id='CEAC-graphic'),
    html.H3('ICER distribution'),
    dcc.Graph(id='CEAC-distribution'),

])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]),pd.DataFrame()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ]),df


#@app.callback(
#    dependencies.Output('strategy1', 'options'),
#    [dependencies.Input('data_loader', 'value')]
#)
#def update_date_dropdown(data_loader):
#    return [{'label': i, 'value': i} for i in data_loader.strategy_dict.keys()]


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children_plus_df = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        children = [x[0] for x in children_plus_df]
        df_list = [x[1] for x in children_plus_df]

        for df in df_list:
            data_loader.load_disease(df)

        #print(children)
        #print(df_list)
        return children


@app.callback(Output('output-data-upload-strategy', 'children'),
            dependencies.Output('strategy1', 'options'),
              dependencies.Output('strategy2', 'options'),
              Input('upload-data-strategy', 'contents'),
              State('upload-data-strategy', 'filename'),
              State('upload-data-strategy', 'last_modified'))
def update_output_strategy(list_of_contents, list_of_names, list_of_dates):

    print('aaaaaas')
    strategy_dict = [{'label': i, 'value': i} for i in data_loader.strategy_dict.keys()]

    if list_of_contents is not None:
        children_plus_df = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        children = [x[0] for x in children_plus_df]
        df_list = [x[1] for x in children_plus_df]

        for df in df_list:
            data_loader.load_strategies(df)

        print(df)


        return children,strategy_dict,strategy_dict

    else:
        return None,strategy_dict,strategy_dict


#@app.callback(
#    Output('out_total_cost1', component_property='children'),
#    Output('out_total_cost2', component_property='children'),
#    Output('out_life_exp1', component_property='children'),
#    Output('out_life_exp2', component_property='children'),
#    Output('out_icer', component_property='children'),
#    Input('in_total_cost1', component_property='value'),  # ,suppress_callback_exceptions=True),
#    Input('in_total_cost2', component_property='value'),  # ,suppress_callback_exceptions=True)
#    Input('in_life_exp1', component_property='value'),  # ,suppress_callback_exceptions=True),
#    Input('in_icer', component_property='value'),  # ,suppress_callback_exceptions=True)
#    Input('in_life_exp2', component_property='value')  # ,suppress_callback_exceptions=True)
#)
#def update_output_div(input_value1, input_value2, life1, life2, icer):
#    return input_value1, input_value2, life1, life2, icer


@app.callback(
    Output('CEAC-graphic', 'figure'),
    Output('CEAC-distribution', 'figure'),
    Output('in_total_cost1', 'children'),
    Output('in_total_cost2', 'children'),
    Output('in_life_exp1', 'children'),
    Output('in_life_exp2', 'children'),
    Output('in_icer', 'children'),
    Input('strategy1', 'value'),
    Input('strategy2', 'value'),
    Input('strategy1_cost', 'value'),
    Input('strategy2_cost', 'value'),
    Input('intervention_probability_bounds', 'value'),
    Input('intervention_cost', 'value'),
    Input('eps_cs_bounds', 'value'),
    Input('eps_pgt_bounds', 'value')
)
def update_graph_CEAC(strategy1, strategy2, strategy1_cost, strategy2_cost, intervention_bounds, intervention_cost,
                      eps_cs_bounds, eps_pgt_bounds):
    print(intervention_bounds)
    rho_notint_lb = 1 - intervention_bounds[1]
    rho_notint_ub = 1 - intervention_bounds[0]

    # fig = px.scatter(x=[0,1,3],
    #                 y=[2,8,4],
    #                 hover_name=['a','b','c'])

    strat1 = data_loader.strategy_dict[strategy1]
    strat2 = data_loader.strategy_dict[strategy2]

    psa = Psa(strat1, strat2)
    disease_space = list(set(strat1.disease_list).union(strat2.disease_list))  # ['disease1', 'disease2', 'disease3']
    psa.run_mc(disease_space=disease_space,
               intervention_cost_lb=intervention_cost[0], intervention_cost_ub=intervention_cost[1],
               testing_cost1_lb=strategy1_cost[0], testing_cost1_ub=strategy1_cost[1],
               testing_cost2_lb=strategy2_cost[0], testing_cost2_ub=strategy2_cost[1],
               eps_cs_lb=eps_cs_bounds[0], eps_cs_ub=eps_cs_bounds[1],
               eps_pgt_lb=eps_pgt_bounds[0], eps_pgt_ub=eps_pgt_bounds[1],
               rho_notint_lb=rho_notint_lb, rho_notint_ub=rho_notint_ub, nsim=10000)

    # fig = px.histogram(psa.icer_mc_samples)

    # Create random data with numpy
    import numpy as np
    from plotly.subplots import make_subplots

    # Create traces
    # fig = go.Figure()
    fig = px.ecdf({'cost effectiveness probability ': psa.icer_mc_samples},
                  labels={'value': 'ICER threshold (Euros/Gained Year)', 'b': 'b',
                          'variable': 'legend'})  # ,fig=fig)#df, x="total_bill")
    fig.add_trace(go.Scatter(x=[psa.icer_deterministic, psa.icer_deterministic], y=[0, 1],
                             mode='lines',
                             name='deterministic ICER'))

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_histogram(x=psa.icer_mc_samples, secondary_y=True, name='montecarlo samples')

    fig2.add_trace(go.Scatter(x=[psa.icer_deterministic, psa.icer_deterministic], y=[0, 1],
                              mode='lines',
                              name='deterministic ICER'))

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    total_cost1 = psa.total_cost1_deterministic
    total_cost2 = psa.total_cost2_deterministic
    life_exp1 = psa.life_exp1_deterministic
    life_exp2 = psa.life_exp2_deterministic

    return fig, fig2, total_cost1, total_cost2, life_exp1, life_exp2, psa.icer_deterministic


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8052)
