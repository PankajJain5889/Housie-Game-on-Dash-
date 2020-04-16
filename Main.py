import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from playerCard import playerCard
cols = ['Column_'+str(x) for x in range(10)]
rows = ['Row_'+str(x) for x in range(10)]
visited = []
unvisited = np.arange(100)
for _ in range(20):
    np.random.shuffle(unvisited)
df = pd.DataFrame(index = rows, columns=cols)
current_num = -1
count=0
for x in range(len(rows)):
    for y in range(len(cols)):
        df['Column_'+str(y)][x] = '***Blocked***'
        count+=1
Num_players=0
currentPlayers = []
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Welcome To Housie App'   ,style={'color': 'blue', 'fontSize': 24 ,'textAlign' : 'center' }),  
 	dash_table.DataTable(
 		style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
    	},
    style_cell={'textAlign': 'center'},
    id='Main_Table', 
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
)  ,
html.H1(id = 'CurrentNum',children=	"Currently Selected number:"+str(current_num),style={'color': 'blue', 'fontSize': 24 ,'textAlign' : 'left' }),
html.Button('Pick a number', id='pickButton'),
html.Br(),
dcc.Input(id='PlayerName', value='', type='text'),
html.Br(),
html.Button(id='addPlayerButton', type='submit', children='Add a Player'),
html.Br(),
html.Div(id = 'currentPlayers',children=[])
])

@app.callback(Output('currentPlayers', 'children'),
    [Input('addPlayerButton', 'n_clicks')],
    [State('currentPlayers' ,'children'),
    State('PlayerName' , 'value')]
)
def addPlayers(n_clicks , children , playerName):
	global currentPlayers
	if n_clicks:
		if playerName in [x.name for x in currentPlayers]:
			children.append("Duplicate name exists!!!!")
			return children
		player = playerCard(playerName)
		currentPlayers.append(player)
		cols = ['Column_'+str(x) for x in range(9)]
		rws = ['row_'+str(x) for x in range(6)]
		df = pd.DataFrame(index= rws, columns = cols)
		for i,r in enumerate(rws):
			for j,c in enumerate(cols):
				if player.ticket[i][j]>-1:
					df[c][r] = str(int(player.ticket[i][j]))
				else:
					df[c][r] = ' '
		children.append(html.H1(children=player.name, style={'color': 'blue', 'fontSize': 24 ,'textAlign' : 'center' }))
		children.append(html.Br())			
		children.append(
			dash_table.DataTable(
 		style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
    	},
    style_cell={'textAlign': 'center'},
    id=player.name, 
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
))
	return children

@app.callback(Output('CurrentNum', 'children'),
    [Input('pickButton', 'n_clicks')],

)
def random_button(n_clicks ):
	#df = pd.DataFrame(df)
	
	if n_clicks:
		
		global unvisited
		global visited
		global current_num
		if len(unvisited):
		    visited.append(unvisited[-1])
		    current_num = visited[-1]
		    unvisited = unvisited[:-1]
		else:
			current_num = None
			print("End of game")
		
	s = "Currently Selected number:"+str(current_num)
	return s
	
@app.callback(Output('Main_Table', 'data'),
    [Input('CurrentNum', 'children')],
    [State('Main_Table', 'data')]
)
def update_table(num , df):
	num = int(num.split(":")[-1])
	df = pd.DataFrame(df)
	global visited
	if len(visited):
		if num >=10:
			x , y = (num//10) , (num%10)
		else:
			x ,y = 0 , num
		df['Column_'+str(y)][x] = num
	return df.to_dict('records')
if __name__ == '__main__':
    app.run_server(debug=True)
		