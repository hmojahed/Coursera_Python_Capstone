# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(id='payload-slider', allowCross=False,
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500',
                                            10000: '10000'},
                                    value=[0, 10000])
                                ]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
            Output(component_id='success-payload-scatter-chart', component_property='figure')],
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value')])

#@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
#            Output(component_id='success-payload-scatter-chart', component_property='figure')],
#            [Input(component_id='site-dropdown', component_property='value'),
#             Input(component_id='payload-slider', component_property='value')],
#            [State('success-pie-chart', 'figure'), 
#            State('success-payload-scatter-chart', 'figure')]
#              )

#def get_pie_chart(entered_site, slider_value, o1, o2):
def get_pie_chart(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launces by Site')
        
        #fig2 = px.pie(spacex_df, values='class', 
        #names='Launch Site', 
        #title='Total Success Launces by Site')

        fig2 = px.scatter(spacex_df, x=spacex_df['Payload Mass (kg)'], y=spacex_df['class'], 
        color ='Booster Version Category', 
        title='Correlation between Payload and Success for all sites') 
        return (fig, fig2)
    else:
        
        filtered_df ['size'] = np.zeros(56)
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['Launch Site', 'class'], as_index=False).count().reset_index()
        
        fig = px.pie(filtered_df, values='size', 
        names='class', 
        title='Total Success Launces for site '+ entered_site)

        filtered_df2 = spacex_df[spacex_df['Launch Site']==entered_site]

        fig2 = px.scatter(filtered_df2, x=filtered_df2['Payload Mass (kg)'], y=filtered_df2['class'], 
        color ='Booster Version Category', 
        title='Correlation between Payload and Success for '+ entered_site) 
        fig2.update_xaxes(range = payload_range)

        return (fig, fig2)
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#def get_scatter_chart(entered_site2):
#    filtered_df = spacex_df
#    if entered_site2 == 'ALL':
#        #px.scatter(df2, x=df2.index, y=df2.columns)
#        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', 
#        color ="Booster Version Category", 
#        title='Correlation between Payload and Success for all sites') 
#        return fig
#    else:
        
        #filtered_df ['size'] = np.zeros(56)
        #filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['Launch Site', 'class'], as_index=False).count().reset_index()
        

        #fig = px.pie(filtered_df, values='size', 
        #names='class', 
        #title='Total Success Launces for site '+ entered_site)
 #       return fig                             


# Run the app
if __name__ == '__main__':
    app.run_server()
