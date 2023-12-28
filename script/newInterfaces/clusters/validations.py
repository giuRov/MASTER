from datetime import datetime, timedelta
from multiprocessing import Value
from pickle import TRUE
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash                                     # pip install dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.io as pio
import base64
from PIL import Image

pio.templates.default = "plotly_white" 
#pio.templates.default = "plotly_dark" 

# Data 
directory = '/Users/giuliarovinelli/Desktop/Università/PhD/actv/actvData/script/codeMASTER/MASTER/transformData/'
timeSlots = pd.read_csv(directory+'timeSlots.csv')
validations = pd.read_csv(directory+'validations.csv')

cluster_colors = {
    0: 'blue',
    1: 'green',
    2: 'red',
    3: 'orange',
    4: 'purple',
    5: 'cyan',
    6: 'magenta',
    7: 'yellow',
    8: 'black',
    9: 'gray',
    10: 'lightblue',
    11: 'lightgreen',
    12: 'pink',
    13: 'brown',
    14: 'darkblue',
    15: 'darkgreen',
    16: 'salmon',
    17: 'gold',
    18: 'violet',
    19: 'teal',
    20: 'olive',
    21: 'navy',
    22: 'lime',
    23: 'indigo',
    24: 'orchid',
}

cluster_names = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: '11',
    12: '12',
    13: '13',
    14: '14',
    15: '15',
    16: '16',
    17: '17',
    18: '18',
    19: '19',
    20: '20',
    21: '21',
    22: '22',
    23: '23',
    24: '24',
    25: '25',
    26: '26',
    27: '27',
    28: '28',
    29: '29',
    30: '30',
    31: '31'
}

custom_colors = {
    0: '#636EFA',
    1: '#EF553B',
    2: '#00CC96',
    3: '#AB63FA',
    4: '#FFA15A',
    5: '#19D3F3'
}

image_path = '/Users/giuliarovinelli/Desktop/Università/PhD/actv/actvData/script/codeMASTER/MASTER/script/newInterfaces/MASTERlogo.png'
#Using Pillow to read the the image
pil_img = Image.open("/Users/giuliarovinelli/Desktop/Università/PhD/actv/actvData/script/codeMASTER/MASTER/script/newInterfaces/MASTERlogo.png")

# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(children=[
        html.Img(src=b64_image(image_path), style={'width': '400px', 'height': '200px', 'margin-bottom': '20px'}),
        html.Br(),
        html.Label('Period'),
        dcc.Dropdown(
            id='my-dynamic-period',
            options=[{'label': 'Carnival', 'value': 'Carnival'}, 
                     {'label': 'Easter', 'value': 'Easter'},
                     {'label': 'Spring', 'value': 'Spring'},
                     {'label': 'Summer', 'value': 'Summer'}],
            multi=False,
            value='Carnival',
            placeholder="Select a period",
            style={'width': 400, 'align-items': 'left', 'justify-content': 'left'}
        ),
        html.Br(),
        html.Label('Ticket'),
        dcc.Dropdown(
            id='my-dynamic-dropdown',
            multi=False,
            value='all tickets',
            placeholder="Select a ticket type",
            style={'width': 400, 'align-items': 'left', 'justify-content': 'left'}
        ),
    ],style={'padding': 10, 'flex': 10}),

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='mymap'),
                ],
                style={'padding': 10}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='bar-chart', clickData=None),
                        ],
                        style={'width': '50%', 'display': 'inline-block', 'padding': 9}
                    ),
                    html.Div(
                        [
                        html.Br(),
                        html.Label('Stop'),
                        dcc.Dropdown(
                            id='my-dynamic-stop',
                            multi=False,
                            placeholder="Select a stop",
                            value='Lido bus', # Posso mettere a mano 'Lido bus' perche' nell'interfaccia so che partiremo con 'Carnival' e 'All tickets'
                            style={'width': 150, 'align-items': 'right', 'justify-content': 'right'}
                        ),
                            dcc.Graph(id='pie-chart', clickData=None),
                        ],
                        style={'width': '40%', 'display': 'inline-block', 'margin-left': '80px'}
                    ),
                ],
                style={'display': 'flex', 'padding': 10}
            ),
        ],
        style={'display': 'flex', 'flex-direction': 'column', 'flex': 8}  # Adjust flex value for sizing
    ),
], style={'display': 'flex', 'flex-direction': 'row'})


@app.callback(
    Output('my-dynamic-dropdown', 'options'),
    Output('my-dynamic-dropdown', 'value'),
    Input('my-dynamic-period', 'value')
)
def update_options(selected_period):
    if selected_period == 'Summer':
        reduced_options = [
            {'label': 'All tickets', 'value': 'all tickets'},
            {'label': '75 minutes', 'value': '75 minutes'},
            {'label': 'Residents', 'value': 'residents'},
            {'label': 'Tourists', 'value': 'tourists'}
        ]
        return reduced_options, 'all tickets'  # Set default value for Summer
    else:
        full_options = [
            {'label': 'All tickets', 'value': 'all tickets'},
            {'label': '75 minutes', 'value': '75 minutes'},
            {'label': 'Residents', 'value': 'residents'},
            {'label': 'Students', 'value': 'students'},
            {'label': 'Workers', 'value': 'workers'},
            {'label': 'Tourists', 'value': 'tourists'},
            {'label': 'Retirees', 'value': 'retirees'}
        ]
        return full_options, 'all tickets'  # Set default value for other periods

    
@app.callback(
    Output('my-dynamic-stop', 'options'),
    Input('my-dynamic-period', 'value'),
    Input('my-dynamic-dropdown', 'value')
)
def update_dropdown2_options(period,value):
    df = validations.copy()
    mask = ((df['PERIODO'] == period) & (df['TIPOLOGIA'] == value))
    df = df.loc[mask]

    return [
        {'label': i, 'value': i}
        for i in df['DESCRIZIONE'].unique()
    ]

@app.callback(
    Output(component_id='mymap', component_property='figure'),
    Input(component_id='my-dynamic-period', component_property='value'),
    Input(component_id='my-dynamic-dropdown', component_property='value')
)
def update_output(period,value):
    df = validations.copy()
    mask = ((df['PERIODO'] == period) & (df['TIPOLOGIA'] == value))
    df = df.loc[mask]
    df['Color'] = df['CLUSTER'].map(cluster_colors)

    # Grouping by 'CLUSTER' and counting occurrences
    cluster_counts = df.groupby('CLUSTER').size().reset_index(name='COUNTS')
    df = pd.merge(df, cluster_counts, on='CLUSTER')

    center_lat = np.mean(df['LATITUDE'])
    center_lon = np.mean(df['LONGITUDE'])
    df['CLUSTER'] = df['CLUSTER'].astype(str)
    fig = px.scatter_mapbox(df, lat='LATITUDE', lon='LONGITUDE', color="CLUSTER", size = 'COUNTS', 
                            mapbox_style="carto-positron", width=1250, height=500, zoom=11,
                            center = {'lon': center_lon, 'lat': center_lat},
                            hover_data={'LATITUDE': False,'LONGITUDE':False,'DESCRIZIONE':True,'CLUSTER': True, 'Color': False, 'COUNTS': False},
                            color_discrete_map=cluster_names,
                            )
    fig.update_layout(
        margin={'t': 0,'l':0,'b':0,'r':40}
	)
    # Create custom legend annotations
    clusters = df['CLUSTER'].unique()
    cluster_positions = list(range(len(clusters)))

    for cluster, position in zip(clusters, cluster_positions):
        fig.add_annotation(
            xref='paper', yref='paper',
            x=1.1, y=0.9 - (position * 0.05),  # Adjust position
            text=f"{cluster}",
            showarrow=False,
            font=dict(color='black', size=10)
        )
    return fig

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    Input(component_id='my-dynamic-period', component_property='value'),
    Input(component_id='my-dynamic-dropdown', component_property='value')#, 
)
def update_output_sec(period,value):
    df = timeSlots.copy()
    my_time_min = df.start.min()
    my_time_max = df.start.max()
    mask = ((df['period'] == period) & (df['typology'] == value))
    df = df.loc[mask]

    df['start-end'] = df['start'] + '-' + df['end']
    df['cluster_id'] = df['cluster_id'].astype('category')
    fig2 = px.bar(df,x='tot_validations',y='start-end',hover_data=['tot_validations'],color='cluster_id',
                  color_discrete_map=custom_colors,text_auto='.2s',
                  height=400,width=700,labels={'time':'Time slots', "cluster_id": "Time Slots"})
    #labels={'counts':'Number of tickets'})
    fig2.update_layout(
        margin={'t': 15,'l':0,'b':0,'r':0,'pad':7},
        xaxis=dict(range=[my_time_min,my_time_max],showticklabels=True),
    )
    fig2.update_traces(textfont_size=12, textangle=0.9, textposition="outside", cliponaxis=False)
    fig2.update_xaxes(title_text='Number of validations',title_standoff=30)
    fig2.update_yaxes(title_text='Time slots',title_standoff=30)
    fig2.update_layout(legend=dict(
        x=1.05,  # Position the legend at 100% width of the plot area
        y=1,  # Position the legend at 50% height of the plot area
        traceorder='normal'  # Display legend entries in the order they're provided
    ))
    fig2.update_yaxes(autorange="reversed")
    return fig2


@app.callback(
    Output(component_id='pie-chart', component_property='figure'), 
    [Input(component_id='my-dynamic-period', component_property='value'),
    Input(component_id='my-dynamic-stop', component_property='value'),
    Input(component_id='my-dynamic-dropdown', component_property='value')]
)
def update_output_third(period, stop, value):
    df = validations.copy()
    # Filter the DataFrame based on period and value if needed
    mask = ((df['PERIODO'] == period) & (df['TIPOLOGIA'] == value) & (df.DESCRIZIONE == stop))
    df = df.loc[mask]
    # Aggregate values from columns 0 to 5
    values = [df[str(i)].iloc[0] for i in range(6)]
    labels = [i for i in range(6)]
    # Create a pie chart using Plotly Express
    fig = px.pie(
        values=values,
        names=labels,
        color = labels,
        color_discrete_map=custom_colors,
        #title='Distribution of validations in the 5 time slots for the selected stop'
    )
    fig.update_layout(showlegend=False,
                      width=500,  # Width of the entire chart area
                      height=350,
                      margin=dict(l=45, r=50, b=50, t=0))  # Height of the entire chart area)
    fig.update_traces(textposition='inside', textinfo='percent')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)

