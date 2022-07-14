#!/usr/bin/env python3

"""
Follow relion live
Rafael Fernandez-Leiro & Nayim Gonzalez-Rodriguez 2022
"""

"""
Activate conda environment before running
relion_live.py should be run from relion's project directory
if your folder has lots of jobs might take a while to load!
"""

### Setup
import os
import pandas as pd
import starfile
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import socket
import argparse

# Parsing port number, host and debug mode
parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", help = "choose port to run the webapp")
parser.add_argument("--host", "-host", help = "choose host to run the webapp")
parser.add_argument("--debug", "-d", help = "launch app in debug mode")
args, unknown = parser.parse_known_args()

# Set localhost and 8050 as host and port by default
if not args.port: port_number = 8050
else: port_number = args.port
if not args.host: hostname = socket.gethostname()
else: hostname = args.host
if not args.debug: debug_mode = False
else: debug_mode = args.host

## Function Definitions
# Scatter plots
def plot_scatter(df, range_y, range_x, title_y, color):
    plot = px.scatter(
        data_frame = df,
        range_y = (range_y),
        range_x = (range_x),
        y = title_y,
        color_discrete_sequence = [color],
        marginal_y="histogram",
        hover_data=[title_y],
        orientation = 'h',
        render_mode = 'webgl',
        template = 'plotly_white',
        height = 220, #maybe this can be done in a different way?
    )
    plot.update_layout(xaxis={"showgrid": False}, yaxis={"showgrid": True})
    return plot

## Style
# Header
header_style = {'width': '29%', 'display': 'inline-block', 'vertical-align': 'middle'}
title1_style = {"margin-left": "15px", "margin-top": "15px", "margin-bottom": "0em", "color": "Black",
                "font-family" : "Helvetica", "font-size":"2.5em"}
title2_style = {"margin-left": "15px", "margin-top": "0em", "color": "Black", "font-family" : "Helvetica"}
progress_style = {'width': '70%', 'display': 'inline-block', 'vertical-align': 'top' , 'marginBottom':0, 'marginTop':-25}

# Tabs
general_text_style = {"margin-left": "15px", "color": "Black", "font-family" : "Helvetica", 'display': 'inline-block'}
tabs_style = {'height': '3em', 'width': '100%', 'display': 'inline', 'vertical-align': 'bottom', 'borderBottom':'3px #000000'}
tab_style = {'padding':'0.5em', "font-family" : "Helvetica", 'background-color':'white'}
tab_selected_style = {'padding':'0.5em', 'borderTop': '3px solid #000000', "font-family" : "Helvetica", 'font-weight':'bold'}

# Colors definitions
color_ctf1 = 'cornflowerblue'
color_ctf2 = 'lightblue'
color_ice1 = 'cornflowerblue'
color_motion1 = 'salmon'
color_motion2 = 'lightsalmon'





### Project directory

relion_wd = os.getcwd()

print('starting up relion_live dashboard in '+str(relion_wd)+ ' ...')

### Initialising dash APP

assets_path = relion_wd # this reads the whole folder (!!) so takes long if it is a big project 

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
        html.H1("RELION", style=title1_style),
        html.H2("Live Dashboard", style=title2_style),
        ], style=header_style),
    html.Div([
        dcc.Graph(id='progress_graph', figure={}),
        ], style=progress_style),
        
    #Live updates
    dcc.Interval(
        id='interval-component',
        interval=15*1000, # in milliseconds
        n_intervals=0
        ),

    ## Tabs

    dcc.Tabs(style=tabs_style, children=[

        ## Tab Live Data

        dcc.Tab(label='Live Data', style=tab_style, selected_style=tab_selected_style, children=[

            ## Working directory

            html.H5("Relion working directory: "+relion_wd, style=general_text_style),
            html.Br(),

            ## Import / MC / CtfFind job folder inputs

            html.H5("Import Job:", style=general_text_style),
            dcc.Input(id='import_name', type='text', value='job001', debounce=True, style=general_text_style),
            html.H5("MotionCorr Job:", style=general_text_style),
            dcc.Input(id='motion_name', type='text', value='job002', debounce=True,style=general_text_style),
            html.H5("CtfFind Job:", style=general_text_style),
            dcc.Input(id='ctf_name', type='text', value='job003', debounce=True, style=general_text_style),
            html.H5("IceFind Job:", style=general_text_style),
            dcc.Input(id='ice_name', type='text', value='job005', debounce=True, style=general_text_style),
            html.Br(), 


            ## Graphs
            html.H5("General x-axis range:", style=general_text_style),
            dcc.RangeSlider(id='xrange', min=0, max=300, step=1, value=[], marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),

            html.H5("Total motion", style=general_text_style),
            dcc.RangeSlider(id='totalmotion_minmax', min=0, max=300, step=1, value=[0,200], marks=None,
                            tooltip={"placement": "left", "always_visible": True}),
            dcc.Graph(id='totalmotion_graph', figure={}),

            html.H5("Defocus", style=general_text_style),
            dcc.RangeSlider(id='defocus_minmax', min=0, max=6, step=0.2, value=[0,4], marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='defocus_graph', figure={}),

            html.H5("Astigmatism", style=general_text_style),
            dcc.RangeSlider(id='astigmatism_minmax', min=-0.05, max=0.1, step=0.01, value=[0,0.05],  marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='astigmatism_graph', figure={}),

            html.H5("Max Resolution", style=general_text_style),
            dcc.RangeSlider(id='maxres_minmax', min=0, max=60, step=0.5, value=[0,8],  marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='maxres_graph', figure={}),

            html.H5("CTF figure of merit", style=general_text_style),
            dcc.RangeSlider(id='fom_minmax', min=0, max=0.5, step=0.02, value=[0,0.25],  marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='fom_graph', figure={}),

            html.H5("Ice thickness", style=general_text_style),
            dcc.RangeSlider(id='ice_minmax', min=0, max=5, step=0.1, value=[0,2],  marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='ice_graph', figure={}),

            ]),

        ## Tab Micrographs

        dcc.Tab(label='Micrographs', style=tab_style, selected_style=tab_selected_style, children=[

            html.Br(),

            ### Input Index to select image (or central image?)

            html.H4("Select Image on slider or use <-- --> keys to navigate!", style=general_text_style),
            html.H4("FOR NOW APP NEEDS TO BE RUN IN RELION DIRECTORY FOR IMAGES TO WORK", style=general_text_style),
            dcc.Slider(id='image_index', min=1, max=1, step=1, value=1, marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}),

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
     Output(component_id='ice_minmax', component_property='max'),
     Output(component_id='ice_minmax', component_property='value'),
     Output(component_id='ice_graph', component_property='figure'),
     Output(component_id='mic_jpeg', component_property='src'),
     Output(component_id='ctf_jpeg', component_property='src'),
     Output(component_id='image_index', component_property='max'),
     Output(component_id='progress_graph', component_property='figure')],
    [Input(component_id='xrange', component_property='value'),
     Input(component_id='totalmotion_minmax', component_property='value'),
     Input(component_id='import_name', component_property='value'),
     Input(component_id='motion_name', component_property='value'),
     Input(component_id='defocus_minmax', component_property='value'),
     Input(component_id='astigmatism_minmax', component_property='value'),
     Input(component_id='maxres_minmax', component_property='value'),
     Input(component_id='fom_minmax', component_property='value'),
     Input(component_id='ice_minmax', component_property='value'),
     Input(component_id='ctf_name', component_property='value'),
     Input(component_id='ice_name', component_property='value'),
     Input(component_id='image_index', component_property='value'),
     Input(component_id='interval-component', component_property='n_intervals')]
)

# all inputs in

def load_df_and_graphs(xrange_minmax_values,totalmotion_minmax_values, import_value,
                       motion_value, defocus_minmax_values, astigmatism_minmax_values,
                       maxres_minmax_values, fom_minmax_values, ice_minmax_values, ctf_value, ice_value, index_value, nintervals):

    ### Read dataframes from Import, MotionCorr and CtfFind star files

    importstar = (relion_wd)+'/Import/'+(import_value)+'/movies.star'
    motionstar = (relion_wd)+'/MotionCorr/'+(motion_value)+'/corrected_micrographs.star'
    ctfstar = (relion_wd)+'/CtfFind/'+(ctf_value)+'/micrographs_ctf.star'
    icestar = (relion_wd)+'/External/'+(ice_value)+'/micrographs_ctf_ice.star'

    import_df = starfile.read(importstar)['movies']
    motion_df = starfile.read(motionstar)['micrographs']
    ctf_df = starfile.read(ctfstar)['micrographs']
    ice_df = starfile.read(icestar)['micrographs']

    ctf_df['rlnDefocusU']=round(ctf_df['rlnDefocusU']*0.0001,3)
    ctf_df['rlnCtfAstigmatism']=round(ctf_df['rlnCtfAstigmatism']*0.0001,3)
    ctf_df['rlnCtfMaxResolution']=round(ctf_df['rlnCtfMaxResolution'],1)
    ctf_df['rlnCtfFigureOfMerit']=round(ctf_df['rlnCtfFigureOfMerit'],3)

    ctf_dff = ctf_df.copy()
    motion_dff = motion_df.copy()
    ice_dff = ice_df.copy()


    ### Sliders and graphs

    # Partsing data
    xrangemax = len(import_df)
    xrangeminmax = (xrange_minmax_values)

    motionmax = max(motion_df['rlnAccumMotionTotal'])+10
    motionminmax = (totalmotion_minmax_values)

    defocusmax = max(ctf_df['rlnDefocusU'])+1
    defocusminmax = (defocus_minmax_values)

    astigmatismmax = max(ctf_df['rlnCtfAstigmatism'])+0.1
    astigmatismminmax = (astigmatism_minmax_values)

    maxresmax = max(ctf_df['rlnCtfMaxResolution'])+1
    maxresminmax = (maxres_minmax_values)

    fommax = max(ctf_df['rlnCtfFigureOfMerit'])+0.1
    fomminmax = (fom_minmax_values)

    icemax = max(ice_df['rlnMicrographIceThickness'])+0.1
    iceminmax = (ice_minmax_values)


    # Plotting follow data
    totalmotion = plot_scatter(motion_dff, totalmotion_minmax_values, xrange_minmax_values, 'rlnAccumMotionTotal', color_motion1)
    defocus = plot_scatter(ctf_dff, defocus_minmax_values, xrange_minmax_values, 'rlnDefocusU', color_ctf1)
    astigmatism = plot_scatter(ctf_dff, astigmatism_minmax_values, xrange_minmax_values, 'rlnCtfAstigmatism', color_ctf1)
    maxres = plot_scatter(ctf_dff, maxres_minmax_values, xrange_minmax_values, 'rlnCtfMaxResolution', color_ctf1)
    fom = plot_scatter(ctf_dff, fom_minmax_values, xrange_minmax_values, 'rlnCtfFigureOfMerit', color_ctf1)    
    ice = plot_scatter(ice_dff, ice_minmax_values, xrange_minmax_values, 'rlnMicrographIceThickness', color_ice1)


    # Plotting progress data
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

    return (xrangemax, xrangeminmax, motionmax, motionminmax, totalmotion, defocusmax, defocusminmax,
            defocus, astigmatismmax, astigmatismminmax, astigmatism, maxresmax, maxresminmax, maxres,
            fommax, fomminmax, fom, icemax, iceminmax, ice, mic_jpeg, ctf_jpeg, max_index, progress)

#APP Start

if __name__ == '__main__':
    app.run_server(debug=debug_mode, dev_tools_hot_reload = False, use_reloader=True, host=hostname, port=port_number)
