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
tourists = pd.read_csv(directory+'dataset_compl.csv')

custom_colors = {
    0: '#636EFA',
    1: '#EF553B',
    2: '#00CC96',
    3: '#AB63FA',
    4: '#FFA15A',
    5: '#19D3F3',
    6: '#FF6692',  # Additional color for NUM_DAY 6
    7: '#B6E880',  # Additional color for NUM_DAY 7
    8: '#FFD700',   # Additional color for NUM_DAY 8
}


image_path = '/Users/giuliarovinelli/Desktop/Università/PhD/actv/actvData/script/codeMASTER/MASTER/script/newInterfaces/MASTERlogo.png'
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
                    {'label': 'Spring', 'value': 'Spring'},
                    {'label': 'Summer', 'value': 'Summer'},
                    {'label': 'Easter', 'value': 'Easter'}],
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
            options = [
                {'label': 'One day', 'value': 1},
                {'label': 'Two days', 'value': 2},
                {'label': 'Three days', 'value': 3},
                {'label': 'Seven days', 'value': 4}],
            value=1,
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
    Output('my-dynamic-stop', 'options'),
    Input('my-dynamic-period', 'value'),
    #dInput('my-dynamic-stop', 'value')
)
def update_dropdown2_options(period):
    df = tourists.copy()
    #mask = ((df['PERIODO'] == period) & (df['TIPOLOGIA'] == value))
    mask = (df['PERIODO'] == period)
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
def update_output(period,ticket):
    df = tourists.copy()
    mask = ((df['PERIODO'] == period) & (df['TICKET_CODE'] == ticket))
    df = df.loc[mask]
    # Raggruppamento per 'TICKET_CODE' e conteggio delle righe per ciascun gruppo
    conteggio_per_ticket = df.groupby(['NUM_DAY', 'LATITUDE','LONGITUDE','FERMATA','DESCRIZIONE']).size().reset_index(name='NUM_VALIDATIONS')
    if(ticket == 1 ) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<3
    elif (ticket == 2) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<4
    elif (ticket == 3) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<5
    else :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<9

    conteggio_per_ticket = conteggio_per_ticket.loc[controllo_giorni]
    # Normalizza la colonna 'NUM_VALIDATIONS' per avere valori compresi tra 3 e 10 (dimensione minima e massima dei punti)
    conteggio_per_ticket['normalized_size'] = np.interp(conteggio_per_ticket['NUM_VALIDATIONS'], 
                                                        (conteggio_per_ticket['NUM_VALIDATIONS'].min(),
                                                         conteggio_per_ticket['NUM_VALIDATIONS'].max()), (2, 130)
                                                        )


    center_lat = np.mean(conteggio_per_ticket['LATITUDE'])
    center_lon = np.mean(conteggio_per_ticket['LONGITUDE'])

    fig = px.scatter_mapbox(conteggio_per_ticket, lat='LATITUDE', lon='LONGITUDE', color='NUM_VALIDATIONS', size = 'normalized_size', #min_size=3,
                            mapbox_style="carto-positron", width=1250, height=630, zoom=11,animation_frame = 'NUM_DAY',
                            center = {'lon': center_lon, 'lat': center_lat},
                            hover_data={'LATITUDE': False,'LONGITUDE':False,'DESCRIZIONE':True,'normalized_size':False},
                            color_continuous_scale='viridis',
                            range_color=[conteggio_per_ticket['NUM_VALIDATIONS'].min(),conteggio_per_ticket['NUM_VALIDATIONS'].max()]
                            )
    fig.update_layout(
        margin={'t': 0,'l':0,'b':0,'r':40}
	)
    return fig

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    Input(component_id='my-dynamic-period', component_property='value'),
    Input(component_id='my-dynamic-dropdown', component_property='value')#, 
)
def update_output_sec(period, ticket):
    df = tourists.copy()
    mask = ((df['PERIODO'] == period) & (df['TICKET_CODE'] == ticket))
    df = df.loc[mask]

    # Raggruppamento per 'TICKET_CODE' e conteggio delle righe per ciascun gruppo
    conteggio_per_ticket = df.groupby(['NUM_DAY']).size().reset_index(name='NUM_VALIDATIONS')
    if(ticket == 1 ) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<3
    elif (ticket == 2) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<4
    elif (ticket == 3) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<5
    else :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<9

    conteggio_per_ticket = conteggio_per_ticket.loc[controllo_giorni]
    # Convert NUM_DAY to categorical to ensure discrete colors
    conteggio_per_ticket['NUM_DAY'] = pd.Categorical(conteggio_per_ticket['NUM_DAY'])
    #print(conteggio_per_ticket)

    fig2 = px.bar(conteggio_per_ticket,x='NUM_DAY',y='NUM_VALIDATIONS',#hover_data=['NUM_VALIDATIONS'],
                  color='NUM_DAY',
                  color_discrete_map=custom_colors,
                  #color_continuous_scale='viridis',
                  text_auto='.2s',
                  height=400,width=625,labels={'NUM_VALIDATIONS':'Number of validations', "NUM_DAY": "Day of the ticket"})
    #labels={'counts':'Number of tickets'})
    fig2.update_layout(
        margin={'t': 15,'l':0,'b':0,'r':0,'pad':7},
        #xaxis=dict(range=[my_time_min,my_time_max],showticklabels=True),
    )
    #fig2.update_traces(textfont_size=12, textangle=0.9, textposition="outside", cliponaxis=False)
    fig2.update_xaxes(title_text='Day of the ticket',title_standoff=30) 
    fig2.update_yaxes(title_text='Number of validations',title_standoff=30)
    #fig2.update_layout(legend=dict(
    #    x=1.05,  # Position the legend at 100% width of the plot area
    #    y=1,  # Position the legend at 50% height of the plot area
    #    traceorder='normal'  # Display legend entries in the order they're provided
    #))
    return fig2


@app.callback(
    Output(component_id='pie-chart', component_property='figure'), 
    [Input(component_id='my-dynamic-period', component_property='value'),
    Input(component_id='my-dynamic-stop', component_property='value'),
    Input(component_id='my-dynamic-dropdown', component_property='value')
    ]
)
def update_output_third(period, stop, ticket):
    #df = validations.copy()
    # Filter the DataFrame based on period and value if needed
    #mask = ((df['PERIODO'] == period) & (df['TIPOLOGIA'] == value) & (df.DESCRIZIONE == stop))
    df = tourists.copy()
    mask = ((df['PERIODO'] == period) & (df.DESCRIZIONE == stop) & (df['TICKET_CODE'] == ticket))
    df = df.loc[mask]
    # Raggruppamento per 'TICKET_CODE' e conteggio delle righe per ciascun gruppo
    conteggio_per_ticket = df.groupby(['NUM_DAY']).size().reset_index(name='NUM_VALIDATIONS')
    if(ticket == 1 ) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<3
    elif (ticket == 2) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<4
    elif (ticket == 3) :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<5
    else :
        controllo_giorni = conteggio_per_ticket['NUM_DAY']<9

    conteggio_per_ticket = conteggio_per_ticket.loc[controllo_giorni]

    fig = px.pie(conteggio_per_ticket,
        values='NUM_VALIDATIONS',
        names='NUM_DAY',
        color='NUM_DAY',
        color_discrete_map=custom_colors,
    )
    fig.update_layout(showlegend=True,
                      width=500,  # Width of the entire chart area
                      height=350,
                      margin=dict(l=45, r=50, b=50, t=0))  # Height of the entire chart area
    fig.update_traces(textposition='inside', textinfo='percent',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)

