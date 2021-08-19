# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

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
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                      options=[
                                                          {'label':'All Sites', 'value': 'All Sites'},
                                                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                          {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                          {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                          {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                      ],
                                                      value='All Sites',
                                                      placeholder='Select a Launch Site here',
                                                      searchable=True)),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload,max_payload],
                                                marks={
                                                    0 : {'label' : '0 kg'},
                                                    2500 : {'label' : '2500 kg'},
                                                    5000 : {'label' : '5000 kg'},
                                                    7500 : {'label' : '7500 kg'},
                                                    10000 : {'label' : '10000 kg'}
                                                }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
               # REVIEW4: Holding output state till user enters all the form information. In this case, it will be chart type and year
               
               )
def pie_chart(site):

    if site == 'All Sites':
        launch_succ = spacex_df.groupby('Launch Site').sum(['class']).reset_index()
        pie_fig = px.pie(launch_succ, values='class', names='Launch Site', title='Total Success Launches by Site')

    else:
        launch_data = spacex_df[spacex_df['Launch Site'] == site]
        launch_rate = launch_data['class'].value_counts().reset_index()
        title_str = 'Total Success Launches for site ' + site
        pie_fig = px.pie(launch_rate, values='class', names='index', title=title_str)

    return pie_fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
               )
def scatter_chart(site, slide):
    if site == 'All Sites':
        catplot = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == site]
        catplot = px.scatter(site_data, x='Payload Mass (kg)', y='class', color='Booster Version Category')

    return catplot

# Run the app
if __name__ == '__main__':
    app.run_server()
