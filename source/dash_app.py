# Run this app with `python dash_app_template.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
from psa import Psa
#from cgt_data import *
from load_data import load_data


app = Dash(__name__, suppress_callback_exceptions=True)

disease_dict,strategy_dict = load_data()

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

app.layout = html.Div([

    html.Div([

        html.Div([
            html.H3("Strategy 1"),
            dcc.Dropdown(
                list(strategy_dict.keys()), #['no testing', 'limited testing', 'full testing'],
                list(strategy_dict.keys())[0],
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
                list(strategy_dict.keys()), #['no testing', 'limited testing', 'full testing'],['no testing', 'limited testing', 'full testing'],
                list(strategy_dict.keys())[-1],
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
    html.H3('Deterministic results'),

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

    html.Br(),
    html.H3('CEAC graph'),
    dcc.Graph(id='CEAC-graphic'),
    html.H3('ICER distribution'),
    dcc.Graph(id='CEAC-distribution'),

])


@app.callback(
    Output('out_total_cost1', component_property='children'),
    Output('out_total_cost2', component_property='children'),
    Output('out_life_exp1', component_property='children'),
    Output('out_life_exp2', component_property='children'),
    Output('out_icer', component_property='children'),
    Input('in_total_cost1' , component_property='value'),  # ,suppress_callback_exceptions=True),
    Input('in_total_cost2', component_property='value'),  # ,suppress_callback_exceptions=True)
    Input('in_life_exp1', component_property='value'),  # ,suppress_callback_exceptions=True),
    Input('in_icer', component_property='value'),  # ,suppress_callback_exceptions=True)
    Input('in_life_exp2', component_property='value')  # ,suppress_callback_exceptions=True)
)
def update_output_div(input_value1, input_value2,life1,life2,icer):
    return input_value1, input_value2,life1,life2,icer


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

    strat1 = strategy_dict[strategy1]
    strat2 = strategy_dict[strategy2]

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
    fig = px.ecdf({'cost effectiveness probability ':psa.icer_mc_samples},labels={'value':'ICER threshold (Euros/Gained Year)','b':'b','variable':'legend'})  # ,fig=fig)#df, x="total_bill")
    fig.add_trace(go.Scatter(x=[psa.icer_deterministic, psa.icer_deterministic], y=[0, 1],
                             mode='lines',
                             name='deterministic ICER'))


    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_histogram(x=psa.icer_mc_samples, secondary_y=True,name='montecarlo samples')

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
    app.run_server(debug=True, host="0.0.0.0",port=8051)
