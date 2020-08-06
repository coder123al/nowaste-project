from flask import Flask, render_template, dash, dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


if(__name__=="__main__"):
    app.run(debug=True)