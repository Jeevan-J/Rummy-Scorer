import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash(__name__,meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]

app.layout = html.Div([
    html.H1("Rummy Scorer",style={"text-align":"center"}),
    html.H4('Select Number of Players: '),
    dcc.Dropdown(
        id='number-of-players',
        options=[
            {'label': prop, 'value': prop}
            for prop in [2,3,4,5,6,7]
        ]
    ),

    html.Br(),
    html.H3('Player Names'),

    dash_table.DataTable(
      id="player-names",
      editable=True,
      style_cell={'textAlign': 'left'}
    ),
    
    html.Br(),
    html.H3('Score Board'),
    
    dash_table.DataTable(
      id="score-board",
      editable=True,
      style_cell={'textAlign': 'left','minWidth': '90px', 'width': '180px', 'maxWidth': '180px',}
    ),
    dash_table.DataTable(
      id="score-board-total",
      editable=False ,
      style_header = {'display': 'none'},
      style_cell={'textAlign': 'left','minWidth': '90px', 'width': '180px', 'maxWidth': '180px',}
    )
])

@app.callback(
    [Output('player-names','columns'),
     Output('player-names','data')],
    [Input('number-of-players','value')])
def player_names(value):
    if value:
        columns = ([{'id':str(i), 'name':'Player '+str(i)} for i in range(1,value+1)])
        data = [dict(**{str(i):'Player Name' for i in range(1,value+1)})]
        return [columns,data]
    else:
        return [(),[]]
     
@app.callback(
    [Output('score-board','columns'),
     Output('score-board','data')],
    [Input('player-names','data'),
     Input('number-of-players','value')]) 
def init_score_board(rows,value):
    if value:
        df = pd.DataFrame(rows)
        columns = ([{'id':'Game','name':"Game"}]+[{'id':str(i), 'name':str(i)} for i in df.iloc[0]])
        data = [dict(Game=j,**{str(i):0 for i in df.iloc[0]}) for j in range(1,8)]
        return [columns,data]
    else:
        return [(),[]]

@app.callback(
    [Output('score-board-total','columns'),
     Output('score-board-total','data')],
    [Input('score-board','data'),
     Input('number-of-players','value')]) 
def get_total(rows,value):
    if value:
        df = pd.DataFrame(rows)
        columns = ([{'id':str(i), 'name':str(i)} for i in df.columns])
        data = [dict(Game="Total",**{str(i):sum(pd.to_numeric(df[i])) for i in df.columns if i !="Game"})]
        return [columns,data]
    else:
        return [(),[]]
    
    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0",port=5000,debug=False)