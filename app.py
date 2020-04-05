#!/bin/env python3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from data.finance import get_stock_data, get_dropdown_options

# ===================================
# Create and run App
# ===================================
drop_options = get_dropdown_options()

external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
]
app = dash.Dash(__name__, external_stylesheets=external_css)


app.layout = html.Div([
    # Banner display
    html.Div([
        html.H2(
            'Stock Visualizer',
            id='title'
        )
    ]),

    # Content
    html.Label('Dash Graph'),
    dcc.Dropdown(id='stock-drop', options=get_dropdown_options(), value='AAPL'),
    dcc.Graph(id='graph-close')
])


# ===================================
# Manage Callbacks
# ===================================
@app.callback(Output(component_id='graph-close', component_property='figure'),
              [Input(component_id='stock-drop', component_property='value')])
def update_graph(stock_code):
    """ Callback for every change in Dropdown value"""
    df = get_stock_data(stock=stock_code)
    # trace_close = go.Scatter(x=df.index,
    #                          y=df.Close,
    #                          name='Close',
    #                          line={'color': "#4287f5"})

    trace_close = go.Candlestick(x=df.index,
                                 open=df.Open,
                                 close=df.Close,
                                 high=df.High,
                                 low=df.Low)

    data = [trace_close]  # You can add up more

    # Create plot layout
    layout = {'title': f'Stock price: {stock_code}',
              'showlegend': False,
              'xaxis': go.layout.XAxis(title=go.layout.xaxis.Title(text="Date"), rangeslider=dict(visible=False)),
              'yaxis': go.layout.YAxis(title=go.layout.yaxis.Title(text="Price (USD)"))
              }

    # Create plot
    fig = dict(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
