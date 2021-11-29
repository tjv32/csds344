import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import plotly.graph_objects as go

from make_app import app



body_2 = html.Div(
	[ 
		dbc.Container(
        	[   
                dbc.Row(
                    [
                    	dbc.Col(
	                        [

	                        ]
                    	),
                	]
            	),
                dbc.Row(
                    [
                        dbc.Col(
                            [

                            ]
                    	)
                	]
            	)
            ]
        )
    ]
)

tab_2 = dcc.Tab(
	label='RSA', 
	children=[
        body_2
    ]
)
