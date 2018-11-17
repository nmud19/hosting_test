# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(html.H1("Iris Model Hosting"), style={"text-align": "center"}),
    html.Div([

        html.Label("Sepal Length"),
        dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value='',
            id='sepal-length'
        ),

        html.Label("Sepal Width"),
        dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value='',
            id = 'sepal-width'
        ),

        html.Label("Petal Width"),
        dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value='',
            id = 'petal-width'
        ),

        html.Label("Petal Length"),
        dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value='',
            inputmode = 'numeric',
            id = 'petal-length'
        ),
    ], style={"columnCount" : 2}),
    html.Button('Submit', id='submit'),
    html.Div(id= 'result')
],
    style={
        'width': '65%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'textAlign': 'center',
    }
)

# The functions
@app.callback(
    Output('result', 'children'),
              state = [
                State('petal-width', 'value'),
                State('petal-length', 'value'),
                State('sepal-width', 'value'),
                State('sepal-length', 'value'),
              ],
              events=[Event('submit', 'click')])
def get_predictions(pw, pl, sw, sl):
    """
    Get predictions by source
    :param pw:
    :param pl:
    :param sw:
    :param sl:
    :return:
    """
    arguments = {
        "sepal_length": int(sl),
        "sepal_width": int(sw),
        "petal_length": int(pl),
        "petal_width": int(pw)
    }
    print(arguments)
    from openscoring import Openscoring
    os = Openscoring("http://localhost:8080/openscoring")
    result = os.evaluate("Iris", arguments)

    print(result)
    return html.Div([
        html.H3("The class detected was  : {}".format(result['species'])),
    ])



app.config['suppress_callback_exceptions']=True

if __name__ == '__main__':
    import pandas
    from sklearn.tree import DecisionTreeClassifier
    from sklearn2pmml.pipeline import PMMLPipeline
    from sklearn2pmml import sklearn2pmml

    iris_df = pandas.read_csv("iris.csv")
    #
    pipeline = PMMLPipeline([
        ("classifier", DecisionTreeClassifier())
    ])
    pipeline.fit(iris_df[iris_df.columns.difference(["species"])], iris_df["species"])
    #
    sklearn2pmml(pipeline, "DecisionTreeIris.pmml", with_repr=True)

    ## Actual openscoring code
    from openscoring import Openscoring
    import subprocess

    p = subprocess.Popen('java -jar openscoring-server-executable-1.4.3.jar',
                         shell=True)

    os = Openscoring("http://localhost:8080/openscoring")
    #
    kwargs = {"auth": ("admin", "adminadmin")}
    os.deployFile("Iris", "DecisionTreeIris.pmml", **kwargs)

    app.run_server(debug=True, port=9000)