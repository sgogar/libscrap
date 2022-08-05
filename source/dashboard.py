import pandas as pd
import plotly.express as px
import connector
from dash import Dash, dcc, html

app = Dash(__name__)

conn = connector.create_connector()
c = conn.cursor()

c.execute('''SELECT Book_Language as Language, COUNT(1) as Amount FROM libscrap.libros GROUP BY Book_Language''')

df = pd.DataFrame(c.fetchall(), columns = ['Language', 'Amount'])

#genera graficos
fig = px.bar(df, x="Language", y="Amount")

app.layout = html.Div(children=[
    html.H1(children='LIBGEN'),

    html.Div(children='''
        Shows books by language
    '''),

    dcc.Graph(
        id='languages-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server()