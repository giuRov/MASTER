from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash                                     # pip install dash
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.io as pio

pio.templates.default = "plotly_white" 
#pio.templates.default = "plotly_dark" 

# Data 
directory = '/Users/giuliarovinelli/Desktop/Università/PhD/actv/actvData/data/transformData/'
df_line = pd.read_csv(directory+'df_line.csv')

min_counts = 2000

df_reduce = df_line[df_line['counts']>min_counts]
mask_reduce = (df_reduce['num_stop']== 1)
df_reduce = df_reduce.loc[mask_reduce]
print(f'len(df_reduce): {len(df_reduce)}')
print(df_reduce)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(children=[
        html.H3("ACTV validation", style={'textAlign': 'left'}),
        
        html.Br(),
        html.Label('First stop'),
        dcc.Dropdown(
            id='my-dynamic-dropdown',
            options=df_reduce.start_point.unique(),
            multi=False,
            #value=[0],
            placeholder="Select the first stop of a route",
            style={'width': 400, 'align-items': 'left', 'justify-content': 'left'}
        ),
    ],style={'padding': 10, 'flex': 1}),

    html.Div(children=[
        dcc.Graph(id='mymap'),#,style={'width': '20%','display': 'inline-block'}),#style={'width': '90vh', 'height': '90vh'}),
                                    #'lineHeight': '1px',
                                    #'borderWidth': '1px',
                                    #'borderStyle': 'dashed',
                                    #'borderRadius': '1px'}),
    ]#, style={'padding': 10, 'flex': 1}
    )

])#, style={'display': 'flex', 'flex-direction': 'row'})


@app.callback(
    Output(component_id='mymap', component_property='figure'),
    Input(component_id='my-dynamic-dropdown', component_property='value')#, 
)

def update_output(value):
    print('--------------------- ' + str(datetime.now()) + ' ---------------------')

    dff = df_line[df_line['counts']>min_counts]
    len_choices = len(value)
    if(len_choices == 0) : 
        print("raise PreventUpdate")
        raise PreventUpdate

    #print(f'start_point: {value}')
    mask = (dff['start_point']==value) & (dff['num_stop']== 1)
    dff = dff.loc[mask]
    #print(f'len(dff): {len(dff)}')
    #print(dff)

    id_array = dff.cluster_id.tolist()
    #print(f'id_array: {id_array}')

    df_new = pd.DataFrame(columns=['cluster_id', 'num_stop', 'counts','start_point', 'end_point', 'start_lat','start_lon','end_lat','end_lon'])
    #print(df_new)

    for i in range(len(id_array)) :
        cluster_id = id_array[i]
        mask = (df_line['cluster_id']==cluster_id)
        #frames = [df_new,df_line.loc[mask]]
        #df_new = df_new.append(df_line.loc[mask], ignore_index=True)
        df_new = pd.concat([df_new, df_line.loc[mask]],ignore_index=True)
        
    df_new.drop(columns=['Unnamed: 0'])

    print('df_new')
    print(df_new)
    fig = go.Figure()

    #array_lat = df_new['start_lat'].to_numpy()
    #array_lon = df_new['start_lon'].to_numpy()
    #print(f'array_lat: {array_lat}')
    #print(f'array_lon: {array_lon}')
    #fig = px.scatter_mapbox(dff, lat='lat', lon='lon', color ='counts', size = 'counts', 
    #                        mapbox_style="carto-positron", width=1600, height=700, zoom=12.8,
    #                        color_continuous_scale='viridis',
    #                        range_color=[dff['counts'].min(),dff['counts'].max()],#size_max=50,
    #                        center = {'lon': 12.337817, 'lat': 45.434185},hover_data={'lat': False, 'lon': False,'name':True,'counts': True})

    fig = px.line_mapbox(df_new,lat='start_lat', lon='start_lon', color='stops', zoom=3, height=300,labels={'start_lat': 'lat', 'start_lon': 'lon',
                        'start_point':'Stop name','num_stop': 'Stop number','counts':'Number of tickets'},hover_data={'start_lat': False, 'start_lon': False,'start_point':True,
                        'stops':False,'num_stop':True,'counts': True})

    fig.update_layout(mapbox_style="carto-positron", width=1600, height=700,mapbox_zoom=12,
                        mapbox_center_lat=45.451107,mapbox_center_lon=12.349192,margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_traces(mode='lines+markers')
    for d in fig.data:
        #d.marker.symbol = 'star-triangle-up'
        d.marker.size = 10


    return fig



if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)

