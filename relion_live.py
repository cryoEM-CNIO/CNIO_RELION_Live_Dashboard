#!/usr/bin/env python3

### Setup
import os
import pandas as pd
import starfile
import pathlib
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

### Initialising dash APP

assets_path = os.getcwd()
app = dash.Dash(
    __name__,
    assets_folder=assets_path,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "RELION Live Dashboard"
server = app.server

### APP Layout

app.layout = html.Div([

    ## Title
    html.Div([
        html.H1("RELION Live Dashboard", style={"margin-left": "15px", "color": "CornflowerBlue", "font" : "verdana"}),
        ], style={'width': '29%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        dcc.Graph(id='progress_graph', figure={}),
        ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'middle' , 'marginBottom':0, 'marginTop':-25}),

    #Live updates

    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0
        ),

    ## Tabs

    dcc.Tabs([
        ## Tab Live Data

        dcc.Tab(label='Live Data', children=[

            ## Import / MC / CtfFind job folder inputs

            html.H5("Import Job:", style={"margin-left": "15px", "color": "DimGray", "font" : "verdana", 'display': 'inline-block'}),
            dcc.Input(id='import_name', type='text', value='job001', debounce=True, style={'width':"5%", "margin-left": "15px", "color": "DimGray", "font" : "verdana"}),
            html.H5("MotionCorr Job:", style={"margin-left": "15px", "color": "DimGray", "font" : "verdana",'display': 'inline-block'}),
            dcc.Input(id='motion_name', type='text', value='job002', debounce=True,style={'width':"5%", "margin-left": "15px", "color": "DimGray", "font" : "verdana"}),
            html.H5("CtfFind Job:", style={"margin-left": "15px", "color": "DimGray", "font" : "verdana", 'display': 'inline-block'}),
            dcc.Input(id='ctf_name', type='text', value='job003', debounce=True, style={'width':"5%", "margin-left": "15px", "color": "DimGray", "font" : "verdana"}),

            ## Graphs

            dcc.RangeSlider(id='xrange', min=0, max=300, step=1, value=[],
                            tooltip={"placement": "bottom", "always_visible": True}),

            dcc.RangeSlider(id='totalmotion_minmax', min=0, max=300, step=1, value=[0,200],
                            tooltip={"placement": "left", "always_visible": True}),
            dcc.Graph(id='totalmotion_graph', figure={}),

            dcc.RangeSlider(id='defocus_minmax', min=0, max=6, step=0.2, value=[0,4],
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='defocus_graph', figure={}),

            dcc.RangeSlider(id='astigmatism_minmax', min=-0.05, max=0.1, step=0.01, value=[0,0.05],
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='astigmatism_graph', figure={}),

            dcc.RangeSlider(id='maxres_minmax', min=0, max=60, step=0.5, value=[0,8],
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='maxres_graph', figure={}),

            dcc.RangeSlider(id='fom_minmax', min=0, max=0.5, step=0.02, value=[0,0.25],
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='fom_graph', figure={}),

        ]),

        ## Tab Micrographs

        dcc.Tab(label='Micrographs', children=[

            html.Br(),

            ### Input Index to select image (or central image?)

            html.H4("Select Image", style={"margin-left": "15px", "color": "DimGray", "font" : "verdana", 'display': 'inline-block'}),
            dcc.Slider(id='image_index', min=1, max=1, step=1, value=1, tooltip={"placement": "bottom", "always_visible": True}),

            html.Br(),

            html.Div([
                html.Img(id='mic_jpeg', src='target', height="600", width="900"),
                html.Img(id='ctf_jpeg', src='target', height="600", width="600"),
                ])
            ]),
        ]),
])


### Callbacks (take component ID and properties and connect them)

@app.callback(
    [Output(component_id='xrange', component_property='max'),
     Output(component_id='xrange', component_property='value'),
     Output(component_id='totalmotion_minmax', component_property='max'),
     Output(component_id='totalmotion_minmax', component_property='value'),
     Output(component_id='totalmotion_graph', component_property='figure'),
     Output(component_id='defocus_minmax', component_property='max'),
     Output(component_id='defocus_minmax', component_property='value'),
     Output(component_id='defocus_graph', component_property='figure'),
     Output(component_id='astigmatism_minmax', component_property='max'),
     Output(component_id='astigmatism_minmax', component_property='value'),
     Output(component_id='astigmatism_graph', component_property='figure'),
     Output(component_id='maxres_minmax', component_property='max'),
     Output(component_id='maxres_minmax', component_property='value'),
     Output(component_id='maxres_graph', component_property='figure'),
     Output(component_id='fom_minmax', component_property='max'),
     Output(component_id='fom_minmax', component_property='value'),
     Output(component_id='fom_graph', component_property='figure'),
     Output(component_id='mic_jpeg', component_property='src'),
     Output(component_id='ctf_jpeg', component_property='src'),
     Output(component_id='image_index', component_property='max')],
     Output(component_id='progress_graph', component_property='figure'),
    [Input(component_id='xrange', component_property='value'),
     Input(component_id='totalmotion_minmax', component_property='value'),
     Input(component_id='import_name', component_property='value'),
     Input(component_id='motion_name', component_property='value'),
     Input(component_id='defocus_minmax', component_property='value'),
     Input(component_id='astigmatism_minmax', component_property='value'),
     Input(component_id='maxres_minmax', component_property='value'),
     Input(component_id='fom_minmax', component_property='value'),
     Input(component_id='ctf_name', component_property='value'),
     Input(component_id='image_index', component_property='value'),
     Input(component_id='interval-component', component_property='n_intervals')]
)

# all inputs in

def load_df_and_graphs(xrange_minmax_values,totalmotion_minmax_values, import_value,
                       motion_value, defocus_minmax_values, astigmatism_minmax_values,
                       maxres_minmax_values,fom_minmax_values, ctf_value, index_value,nintervals):

    ### Read dataframes from Import, MotionCorr and CtfFind star files

    print(nintervals)

    importstar = 'Import/'+(import_value)+'/movies.star'
    motionstar = 'MotionCorr/'+(motion_value)+'/corrected_micrographs.star'
    ctfstar = 'CtfFind/'+(ctf_value)+'/micrographs_ctf.star'

    import_df = starfile.read(importstar)['movies']
    motion_df = starfile.read(motionstar)['micrographs']
    ctf_df = starfile.read(ctfstar)['micrographs']

    params = list(ctf_df)
    Total_mics = "Total number of movies: "+str(len(import_df))
    MC_mics = "Motion corrected movies: "+str(len(motion_df))
    CTF_mics = "CTF corrected movies: "+str(len(ctf_df))

    ctf_df['rlnDefocusU']=round(ctf_df['rlnDefocusU']*0.0001,3)
    ctf_df['rlnCtfAstigmatism']=round(ctf_df['rlnCtfAstigmatism']*0.0001,3)
    ctf_df['rlnCtfMaxResolution']=round(ctf_df['rlnCtfMaxResolution'],1)
    ctf_df['rlnCtfFigureOfMerit']=round(ctf_df['rlnCtfFigureOfMerit'],3)

    ctf_dff = ctf_df.copy()
    motion_dff = motion_df.copy()

    ### Colors definitions

    color_ctf1 = 'cornflowerblue'
    color_ctf2 = 'lightblue'
    color_motion1 = 'salmon'
    color_motion2 = 'lightsalmon'

    ### Sliders and graphs

    xrangemax = len(import_df)
    xrangeminmax = (xrange_minmax_values)

    motionmax = max(motion_df['rlnAccumMotionTotal'])+10
    motionminmax = (totalmotion_minmax_values)

    totalmotion = px.scatter(
        data_frame=motion_dff,
        range_y = (totalmotion_minmax_values),
        range_x = (xrange_minmax_values),
        y = 'rlnAccumMotionTotal',
        color_discrete_sequence = [color_motion1],
        marginal_y="histogram",
        hover_data=['rlnAccumMotionTotal'],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220, #maybe this can be done in a different way?
    )

    totalmotion.update_layout(xaxis={"showgrid": False}, yaxis={"showgrid": True})

    defocusmax = max(ctf_df['rlnDefocusU'])+1
    defocusminmax = (defocus_minmax_values)

    defocus = px.scatter(

        data_frame=ctf_dff,
        range_y = (defocus_minmax_values),
        range_x = (xrange_minmax_values),
        color_discrete_sequence = [color_ctf1],
        y = 'rlnDefocusU',
        marginal_y="histogram",
        hover_data=['rlnDefocusU'],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220, #maybe this can be done in a different way?
    )

    defocus.update_layout(xaxis={"showgrid": False}, yaxis={"showgrid": True})


    astigmatismmax = max(ctf_df['rlnCtfAstigmatism'])+0.1
    astigmatismminmax = (astigmatism_minmax_values)

    astigmatism = px.scatter(

        data_frame=ctf_dff,
        range_y = (astigmatism_minmax_values),
        range_x = (xrange_minmax_values),
        y = 'rlnCtfAstigmatism',
        marginal_y="histogram",
        hover_data=['rlnCtfAstigmatism'],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220,
        color_discrete_sequence = [color_ctf1],
    )

    maxresmax = max(ctf_df['rlnCtfMaxResolution'])+1
    maxresminmax = (maxres_minmax_values)

    maxres = px.scatter(

        data_frame=ctf_dff,
        range_y = (maxres_minmax_values),
        range_x = (xrange_minmax_values),
        y = 'rlnCtfMaxResolution',
        marginal_y="histogram",
        hover_data=['rlnCtfMaxResolution'],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220,
        color_discrete_sequence = [color_ctf1],
    )

    fommax = max(ctf_df['rlnCtfFigureOfMerit'])+0.1
    fomminmax = (fom_minmax_values)

    fom = px.scatter(

        data_frame=ctf_dff,
        range_y = (fom_minmax_values),
        range_x = (xrange_minmax_values),
        y = 'rlnCtfFigureOfMerit',
        marginal_y="histogram",
        hover_data=['rlnCtfFigureOfMerit'],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220,
        color_discrete_sequence = [color_ctf1],
    )

    progress = go.Figure()

    progress.add_trace(go.Indicator(
        domain = {'x': [0.15, 0.45], 'y': [0, 1]},
        value = len(motion_df),
        mode = "gauge+number+delta",
        title = {'text': "MotionCorr"},
        delta = {'reference': len(import_df)},
        gauge = {'steps': [{'range': [0,len(import_df)], 'thickness':0.4, 'color':color_motion2}], 'axis': {'range': [None, len(import_df)],'visible': False}, 'borderwidth': 0,  'shape': "bullet", 'bar': {'color': color_motion1,'thickness':0.4}},
        ))

    progress.add_trace(go.Indicator(
        domain = {'x': [0.55, 0.85], 'y': [0, 1]},
        value = len(ctf_df),
        mode = "gauge+number+delta",
        title = {'text': "CtfFind"},
        delta = {'reference': len(import_df)},
        gauge = {'steps': [{'range': [0,len(import_df)], 'thickness':0.4, 'color':color_ctf2}], 'axis': {'range': [None, len(import_df)],'visible': False}, 'borderwidth': 0,'shape': "bullet",  'bar': {'color': color_ctf1,'thickness':0.4}},
        ))

    progress.update_layout(height=220, )

    ### Select image filenames for index

    idx = (index_value)-1
    mic_file_df = ctf_df['rlnMicrographName']
    ctf_file_df = ctf_df['rlnCtfImage']
    mic_file = mic_file_df[idx].replace('mrc','png')
    ctf_file = ctf_file_df[idx].replace('ctf:mrc','png')
    max_index = len(ctf_df)

    ## Load Images

    mic_jpeg = app.get_asset_url(mic_file)
    ctf_jpeg = app.get_asset_url(ctf_file)

    ## return all outputs

    return (xrangemax, xrangeminmax, motionmax, motionminmax, totalmotion, defocusmax,
            defocusminmax, defocus, astigmatismmax, astigmatismminmax, astigmatism,
            maxresmax, maxresminmax, maxres, fommax, fomminmax, fom, mic_jpeg, ctf_jpeg,
            max_index, progress)

#APP Start

if __name__ == '__main__':
    #app.run_server(debug=True, use_reloader=True, host='10.222.112.48', port=8050)
    app.run_server(debug=False, dev_tools_hot_reload = False, use_reloader=True, host='localhost', port=8050)
