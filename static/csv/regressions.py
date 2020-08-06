from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
#creating multilinear regression model, phew uh oh
df = pd.read_csv('allfinaldata.csv')
df.head() 

#multilinear regression = mlr
mlr_y = df['Food waste per person in pounds']
mlr_x = df[['Income Diversity Index', 'RacialDiversityIndex', 'Poverty Rate']]

ml_regression = LinearRegression()
ml_regression.fit(mlr_x, mlr_y)

y_pred = ml_regression.predict(mlr_x)
y_pred 