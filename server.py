from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

dash_app = dash.Dash(
   __name__,
   server=app,
   routes_pathname_prefix='/dash/'
)
 
df = pd.read_csv("static/csv/DSNY_Monthly_Tonnage_Data.csv")

#dropping stuff and resetting index
df.drop(columns=['REFUSETONSCOLLECTED','PAPERTONSCOLLECTED', 'MGPTONSCOLLECTED', 'LEAVESORGANICTONS','XMASTREETONS', 'SCHOOLORGANICTONS'], inplace=True)
df.set_index(df['MONTH'], inplace=True)
df.drop(columns=['MONTH'], inplace=True)

#removed initial months 1-9 from 1991 to 2018
for i in range(1991, 2018):
  for x in range(1, 10):
    df.drop([str(i)+" / 0" +str(x)],inplace=True)

#removed initial months 10-12 from 1991 to 2018
for i in range(1991,2018):
  for x in range(10,13):
    df.drop([str(i)+" / " +str(x)],inplace=True)

#1990 had weird data so had to big fixed on its own
for i in range(6,10):
  df.drop(["1990 / 0" +str(i)],inplace=True)

for i in range(10, 13):
  df.drop(["1990 / " +str(i)],inplace=True)

#2019
for i in range(1, 10):
  df.drop(["2019 / 0" +str(i)],inplace=True)

for i in range(10, 13):
  df.drop(["2019 / " +str(i)],inplace=True)

#2020
for i in range(1, 8):
  df.drop(["2020 / 0" +str(i)],inplace=True)

df.sort_values(by=['COMMUNITYDISTRICT'], inplace=True)
pd.set_option('display.expand_frame_repr', False)

#next cell
#max rows
pd.set_option("max_rows", None)

#evaluating sum
df.dropna()
summedTotal = pd.DataFrame({
    'Sum':[],
    'Borough':[],
    'District':[]
})

for i in range(1,6):
  for x in range(1,19):
    totalNumberOfDistrict=df.loc[(df['BOROUGH_ID']==i) & (df['COMMUNITYDISTRICT']==x), 'RESORGANICSTONS'].sum() 
    summedTotal = summedTotal.append({'Borough': i,'District': x,'Sum': totalNumberOfDistrict},  ignore_index=True)
    

pd.set_option("max_rows", None)
summedTotal.reset_index(inplace = True) 
summedTotal.drop(columns=['index'], inplace=True)
summedTotal=summedTotal.sort_values(by=['Borough','District'])
for i in range(73,90):
  summedTotal.drop([i], inplace=True)
for i in range(12,18):
  summedTotal.drop([i], inplace=True)
for i in range(30,36):
  summedTotal.drop([i], inplace=True)
for i in range(68,72):
  summedTotal.drop([i], inplace=True)
summedTotal.reset_index(inplace = True) 
summedTotal.drop(columns=['index'], inplace=True)

#next cell
#income
income = pd.read_csv("static/csv/income.csv")
income.drop([57],inplace=True)
result = pd.concat([summedTotal, income], axis=1, sort=False)

#preparing to get other data
indexNames = result[ result['Sum'] == 0.0 ].index
result.drop(indexNames , inplace=True)

result.reset_index(inplace = True) 
result.drop(columns=['index'], inplace=True)

result.drop([5,9,19,20],inplace=True)

result.reset_index(inplace = True) 
result.drop(columns=['index'], inplace=True)

#changed sum
newSum=pd.read_csv("static/csv/updatedSum.csv")
result.drop(columns=['Sum'], inplace=True)
result = pd.concat([result, newSum], axis=1, sort=False)

#second to last data read
finalData=pd.read_csv("static/csv/finalData.csv")
result = pd.concat([result, finalData], axis=1, sort=False)
result.drop(result.columns[4], axis=1, inplace=True)
result=pd.concat([result, newSum], axis=1, sort=False)

#actually last
last=pd.read_csv("static/csv/last.csv")
result = pd.concat([result, last], axis=1,sort=False)
result.drop(columns=['Food waste in tons'], axis=1, inplace=True)
result = pd.concat([result, newSum], axis=1, sort=False)

#next cell

#adding new column of percent
result['Food waste in tons'] = pd.to_numeric(result['Food waste in tons'], errors='coerce')
result['Population'] = pd.to_numeric(result['Population'], errors='coerce')
result['Food waste in tons'] = result['Food waste in tons'].astype(float)
result['Population'] = result['Population'].astype(float)

extra=['Populationaged25withabachelorsdegreeorhigher',	'Populationaged25withouthighschooldiploma',	'Unemployment rate',	'PercentageUnemployment',	'Poverty Rate',	'PercentagePoverty',	'PercentageHouseholdswithchildrenunder18yearsold']
result[extra] = result[extra].apply(pd.to_numeric, errors='coerce')



result["Food waste per person in pounds"]=(result["Food waste in tons"]/result["Population"])*2000

#next cell

#testing
result.drop(columns=['INCOME', 'Median Household Income'],inplace=True)
finalTest=pd.read_csv("static/csv/finalTest.csv")
result = pd.concat([result, finalTest], axis=1, sort=False)
result = result.apply(pd.to_numeric, errors='coerce')

#this results in two NaNs that should not be there, so it needs to be fixed
result.dropna(inplace=True)



#graph start
fig = px.scatter(result, x = 'Median Household Income', y = 'Food waste per person in pounds', title='Food scraps per person by diversity',labels={
                     "Food waste per person in pounds": "Food waste per person(lbs)",
                 })

dash_app.layout = html.Div(children=[

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if(__name__=="__main__"):
    app.run(debug=True)
    dash_app.run_server(debug=True)