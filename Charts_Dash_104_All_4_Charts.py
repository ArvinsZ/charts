import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
# from dash import Dash, dcc, html -- this is previous version
from dash import Dash, html, dcc, callback, Output, Input

# # merging the files
# joined_files = os.path.join('C:\\MANS\\Python_Fita\\Binance_BTCUSDT', '*.csv')
# # A list of all joined files is returned
# joined_list = glob.glob(joined_files) 
# # Joining the files
# df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)

# This is only one month: 
df = pd.read_csv('C:\\MANS\\Python_Fita\\Binance_BTCUSDT\\BTCUSDT-1h-2023-04.csv');
df['open_time_timeformat'] = pd.to_datetime(df['open_time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
df['close_time_timeformat'] = pd.to_datetime(df['close_time'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
df['day'] = pd.to_datetime(df['close_time'], unit='ms').dt.strftime('%d')
df['difference']= df['quote_volume'] - df['taker_buy_quote_volume']
df.drop(['ignore'], axis = 1, inplace = True)
df.head(5)

# here starts Dash code

app = Dash(__name__)

 # CHART1 - High, low, open and close prices of BTCUSDT

def candlestick_chart(start_date, end_date):
    filtered_df = df[(df['close_time_timeformat'] >= start_date) & (df['close_time_timeformat'] <= end_date)]
    
    fig = go.Figure(data=[go.Candlestick(x=filtered_df['close_time_timeformat'],
                                         open=filtered_df['open'],
                                         high=filtered_df['high'],
                                         low=filtered_df['low'],
                                         close=filtered_df['close'])])
    
    fig.update_layout(hovermode='x unified', 
                     autosize=True, #this is overridden by height = 600
                      title={
        'text': f"High, low, open and close prices of BTCUSDT (from {start_date} to {end_date})",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        # plot_bgcolor='lightgray',  # Set background color of the chart
        height=700  # Set height of the chart
        # width=600 possibility to modify height also here
        )
    
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=22,
        font_family="Rockwell"))
    
    fig.update_yaxes(type="log")
    return fig

# Chart1 layout

chart1_layout = html.Div([
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=df['close_time_timeformat'].min(),
        max_date_allowed=df['close_time_timeformat'].max(),
        initial_visible_month=df['close_time_timeformat'].min(),
        start_date=df['close_time_timeformat'].min(),
        end_date=df['close_time_timeformat'].max(),
        display_format='YYYY-MM-DD'
    ),
        html.Div(
            id='chart1-container',
            children=[
                dcc.Graph(
                    id='graph-content',
                    style={'width': '99%', 'margin': 'auto'}  # Adjust the width and margin of the graph component
                )
            ],
            #style={
                # 'background-color': 'lightgray',  # Set background color of the chart container
                # 'margin': '10px',  # Set margin around the chart container
                # 'padding': '20px'  # Set padding within the chart container
            #}
        )
    ],
    style={'backgroundColor': 'black', 'padding': '20px'}  # Modify the overall background color of the layout
    )

# Chart1 callback
@app.callback(Output('graph-content', 'figure'),
              [Input('date-range', 'start_date'),
               Input('date-range', 'end_date')])
def update_graph(start_date, end_date):
    return candlestick_chart(start_date, end_date)

# CHART2 - Close price of BTCUSDT

def line_chart():
    fig = go.Figure([go.Scatter(x=df['close_time_timeformat'], y=df['close'])])
    fig.update_layout(hovermode='x unified', 
                      autosize=True, 
                      title={
            'text': "Close price of BTCUSDT",
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            height=700)
    fig.update_layout(hoverlabel=dict(
            bgcolor="white",
            font_size=22,
            font_family="Rockwell"))
    fig.update_yaxes(type="log")
    fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

# Chart2 layout
chart2_layout = html.Div([
    dcc.Graph(id='graph-content-2', figure=line_chart(), 
              style={'width': '99%', 'margin': 'auto'})
],
style={'backgroundColor': 'grey', 'padding': '20px'})


# CHART3 -  "Quote volume and taker buy quote volume of BTCUSDT and difference"

def chart3():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['close_time_timeformat'],
            y=df['quote_volume'],
            name='quote volume',
            marker_color='rgb(55, 83, 109)'))
    fig.add_trace(go.Bar(x=df['close_time_timeformat'],
            y=df['taker_buy_quote_volume'],
            name='taker buy quote volume',
            marker_color='rgb(26, 118, 255)'))
    fig.add_trace(go.Scatter(x=df['close_time_timeformat'],
            y=df['difference'],
            name='Difference',
            marker_color='rgb(128,0,0)'))
    fig.update_layout(hovermode='x unified', autosize = True, title={
    'text': "Quote volume and taker buy quote volume of BTCUSDT and difference",
    'y':0.85,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=22,
        font_family="Rockwell"))
    fig.update_yaxes(type="log")
    # fig.update_layout(width = 1200, height = 800)
    fig.update_layout(xaxis_rangeslider_visible=True)
    # fig.update_layout(legend=dict(
    #     yanchor="top",
    #     y=-0.1,
    #     xanchor="center",
    #     x=0.5))
    #     fig.show()
    return fig

# Chart3 layout
   
chart3_layout = html.Div([
    dcc.Graph(id='graph-content-3', figure=chart3(), 
              style={'width': '99%', 'margin': 'auto'})
],
style={'backgroundColor': 'black', 'padding': '20px'})


# CHART4 - "Quote volume and taker buy quote volume of BTCUSDT"

def chart4():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['close_time_timeformat'],
                y=df['quote_volume'],
                name='quote volume',
                marker_color='rgb(55, 83, 109)'))
    fig.add_trace(go.Scatter(x=df['close_time_timeformat'],
                y=df['taker_buy_quote_volume'],
                name='taker buy quote volume',
                marker_color='rgb(26, 118, 255)'))
    fig.update_layout(hovermode='x unified', autosize = True, title={
        'text': "Quote volume and taker buy quote volume of BTCUSDT",
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.update_layout(hoverlabel=dict(
        bgcolor="white",
        font_size=22,
        font_family="Rockwell"))
    fig.update_yaxes(type="log")
# fig.update_layout(width = 1200, height = 800)
    fig.update_layout(xaxis_rangeslider_visible=True)
# fig.update_layout(legend=dict(
#     yanchor="top",
#     y=-0.1,
#     xanchor="center",
#     x=0.5))
# fig.show()
# pio.write_html(fig, file='chart_without_difference.html', auto_open=True)
    return fig

# Chart4 layout
   
chart4_layout = html.Div([
    dcc.Graph(id='graph-content-4', figure=chart4(), 
              style={'width': '99%', 'margin': 'auto'})
],
style={'backgroundColor': 'grey', 'padding': '20px'})


# Combine all chart layouts:
combined_layout = html.Div([
    chart1_layout,
    chart2_layout,
    chart4_layout,
    chart3_layout
])

app.layout = combined_layout


if __name__ == '__main__':
    app.run_server(debug=True)
                      

