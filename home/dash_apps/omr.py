import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt
import datetime
import pandas as pd
import plotly.graph_objects as go
import dash_table
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots

df = pd.read_excel("home/dash_apps/data.xlsx")

st = df.sort_values(by='Spend_Array')


Region = list(df.Region.value_counts().index)
#Channel = list(df.Channel.value_counts().index)

RegionList = [{'label':f'{i}','value':f'{i}'} for i in Region]
#ChannelList = [{'label':f'{i}','value':f'{i}'} for i in Channel]

ch = df.groupby(df.Channel).sum()
labs = list(ch.index)
vals = list(ch.Spend_Array)

app = DjangoDash('PieChart',
                add_bootstrap_links=True)

app.layout = html.Div([
        html.Div([
            html.Div(
                html.Div([
                    html.H4('Date'),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        min_date_allowed=dt(1995, 8, 5),
                        start_date = dt(2020,2,18).strftime('%Y-%m-%d'),
                        end_date=datetime.date.today(),
                        style = { 
                            'width': '100%',},    
                    ),
                    html.Div(id='output-container-date-picker-range')
                ]), 
                className='col-md-4'
            ),
            
            html.Div(
                html.Div([
                    html.H4('Region'),
                    dcc.Dropdown(
                        id = 'region-dropdown',
                        options = RegionList,    
                        value = "APAC", 
                        style = { 
                            'width': '100%'},
                        ),
                    ]),
                className='col-md-4'
            ),
            
            html.Div(
                html.Div([
                    html.H4('Country'),
                    dcc.Dropdown(
                        id = 'country-dropdown',
                        value = "Australia (AU)",   
                        ),
                    ]),
                className='col-md-4'
            ),
        ],
        className='row p-4'),
        
        html.Div([
            html.Div([
                html.H4('Channel'),
                dcc.Dropdown(
                        id = 'channel-dropdown',  
                        value = "Channel A ",
                        style = { 
                            'width': '100%'},
                        ),
                html.Div(id='output-channel-dropdown'),
            ],className='col-md-6'),
            html.Div([],className='col-md-6'),
        ],className='row px-4'),
        
        html.Div([
            html.Div([
                html.Br(),
                html.H4('Table'),
                html.Div(id='output-table'),
            ],className='col-md-12'),
        ],className='row px-4'),
        
        html.Div([
            html.Div([
                html.Br(),
                html.Br(),
                html.H4("Channel's Spend Array",className='text-center'),
                html.Div([
                dcc.Graph(
                    id='pie_chart_1',
                    figure={
                        'data':[
                            go.Pie(labels=labs, values=vals, hole=.4),
                        ],
                        'layout':go.Layout(
                            annotations=[dict(text='Before', x=0.5, y=0.5, font_size=15, showarrow=False),])
                        },
                    className="col-md-6",
                    ),     
                
                dcc.Graph(
                    id='pie_chart_2',
                    figure={
                        'data':[
                            go.Pie(labels=labs, values=vals, hole=.4),
                        ],
                        'layout':go.Layout(
                            annotations=[dict(text='After', x=0.5, y=0.5, font_size=15, showarrow=False),])
                        },
                    className="col-md-6",
                    ),   
                ],className='row'),
            ],className='col-md-12'),
        ],className='row px-4'),
        
        html.Div([
            html.Div([
                html.Br(),
                # html.H4('Table'),
                html.Div(id='output-line-graph'),
            ],className='col-md-12'),
        ],className='row px-4'),
    ],
    className='container-fluid'
)

@app.callback(
    dash.dependencies.Output('output-table', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('region-dropdown', 'value'),
     dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('channel-dropdown', 'value'),])
def update_table(start_date, end_date, region, country, channel):
    rs = df[df.Date >= start_date]
    rs = rs[rs.Date <= end_date]
    rs = rs[rs.Channel == channel]
    rs = rs[rs.Country == country]
    rs = rs[rs.Region == region]
    rs = rs[["Country", "Region", "Spend_Array", "Est_Regs", "Est_NCs", "Est_Rev", "ROAS", "Avg_CPR", "m-CPNC", "m-ROAS", "total_transactions"]]
    
    table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in rs.columns],
                    data=rs.to_dict('records'),
                    style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll',
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell={'fontSize':15, 'font-family':'sans-serif'},
                )
    return table

@app.callback(
    dash.dependencies.Output('country-dropdown', 'options'),
    [dash.dependencies.Input('region-dropdown', 'value')])
def update_country(region):
    rs = df[df.Region == region]
    Country = list(rs.Country.value_counts().index)
    CountryList = [{'label':f'{i}','value':f'{i}'} for i in Country]
    return CountryList

@app.callback(
    dash.dependencies.Output('channel-dropdown', 'options'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_country(country):
    rs = df[df.Country == country]
    Channel = list(rs.Channel.value_counts().index)
    ChannelList = [{'label':f'{i}','value':f'{i}'} for i in Channel]
    return ChannelList

@app.callback(
    dash.dependencies.Output('output-line-graph', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('region-dropdown', 'value'),
     dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('channel-dropdown', 'value'),])
def update_graph(start_date, end_date, region, country, channel):
    rs = df[df.Date >= start_date]
    rs = rs[rs.Date <= end_date]
    rs = rs[rs.Channel == channel]
    rs = rs[rs.Country == country]
    rs = rs[rs.Region == region]
    rs = rs[["Country", "Region", "Spend_Array", "Est_Regs", "Est_NCs", "Est_Rev", "ROAS", "Avg_CPR", "m-CPNC", "m-ROAS", "total_transactions"]]
    x_rs = rs[rs['m-ROAS']<1].min()['Spend_Array']
    y_rs = rs[rs['m-ROAS']<1].min()['Est_Regs']
    graph = dcc.Graph(
                    id='line-graph',
                    figure={
                        'data':[
                                go.Scatter(x=rs['Spend_Array'], y=rs['Est_Regs'],mode='lines+markers',name='line-graph'),
                        ],
                        'layout':go.Layout(
                            title='Spend_Array vs Est_Regs of {} ({})'.format(country,channel),
                            xaxis={'title':'Spend Array'},
                            yaxis={'title':'Est Regs'},
                            titlefont = {
                                    "size": 20
                                    },
                            annotations=[dict(x=x_rs,
                                              y=y_rs,
                                              xref="x",
                                              yref="y",
                                              text="Diminshing returns",
                                              showarrow=True,
                                              opacity=0.8,
                                              align="center",
                                              font=dict(
                                                    family="Courier New, monospace",
                                                    size=10,
                                                    color="gray"
                                                    ),
                                              ),]
                            # font = {'color':'black'}
                        )
                    },
                )
    return graph
