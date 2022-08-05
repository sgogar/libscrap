import pandas as pd
import plotly.express as px
import connector
from dash import Dash, dcc, html

app = Dash(__name__)

conn = connector.create_connector()
c = conn.cursor()

c.execute('''SELECT Book_Language as Language, COUNT(1) as Amount FROM libscrap.libros GROUP BY Book_Language''')
df_languages = pd.DataFrame(c.fetchall(), columns = ['Language', 'Amount'])

c.execute('''SELECT Book_Year as Year, COUNT(1) as Amount FROM libscrap.libros GROUP BY Book_Year''')
df_year = pd.DataFrame(c.fetchall(), columns = ['Year', 'Amount'])

df_year = df_year[df_year['Year'] > 0]

#genera graficos
fig_languages_bar = px.bar(df_languages, x="Language", y="Amount")
fig_languages_pie = px.pie(df_languages, values="Amount", names="Language")

fig_languages_bar.update_layout(
    title="BOOKS PER LANGUAGE",
    title_x = 0.5,
    font=dict(
        family="Balto",
        size=16,
        color="#3B39AE"
    )
)

fig_years_bar = px.bar(df_year, x='Year', y='Amount', title="YEARS")
fig_years_pie = px.pie(df_year, values="Amount", names="Year")

fig_years_bar.update_layout(
    title="BOOKS PER YEAR",
    title_x = 0.5,
    font=dict(
        family="Balto",
        size=16,
        color="#3B39AE"
    )
)

print(list(df_year["Year"]))

app.layout = html.Div(children=[
    html.H1(children='LIBGEN'),

    html.Div(children='''
        Shows books by language
    '''),

    dcc.Graph(
        id='languages-bar-graph',
        figure=fig_languages_bar
    ),

    dcc.Graph(
        id='languages-pie-graph',
        figure=fig_languages_pie
    ),

    html.Div(children='''
        Shows books by year
    '''),

    dcc.Graph(
        id='month-bar-graph',
        figure=fig_years_bar
    ),

    dcc.Graph(
        id='month-pie-graph',
        figure=fig_years_pie
    ),    
])

if __name__ == '__main__':
    app.run_server()