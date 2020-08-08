from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly    
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
  return render_template("index.html")
@app.route("/about.html")
def about():
  return render_template("about.html")
@app.route("/contact.html")
def contact():
  return render_template("contact.html")

dash_app = dash.Dash(
   __name__,
   #external_stylesheets=external_stylesheets,
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
result.drop(columns=["PercentageHouseholdswithchildrenunder18yearsold"],inplace=True)

#real
#2014-2017 data
extraYearData=pd.read_csv("static/csv/2014-2017data.csv")
extraYearData.dropna(inplace=True)
extraYearData.drop(columns=["Foodscraps per person"], inplace=True)
extraYearData.reset_index(inplace = True)
result=pd.concat([result, extraYearData], sort=False)
result.drop(columns=["index"],inplace=True)
result.reset_index(inplace=True)
result.drop(columns=["index"],inplace=True)
result = result.apply(pd.to_numeric, errors='coerce')


#graph start
fig = px.scatter(result, x = 'Median Household Income', y = 'Food waste per person in pounds', title='Food scraps per person by wealth',labels={
                     "Food waste per person in pounds": "Food waste per person(lbs)",
                 })

fig2 = px.scatter(result, x = 'RacialDiversityIndex', y = 'Food waste per person in pounds', title='Food scraps per person by diversity',labels={
                     "Food waste per person in pounds": "Food waste per person(lbs)",
                 })
fig3 = px.scatter(result, x = 'Householdswithchildrenunder18yearsold', y = 'Food waste per person in pounds', title='Food scraps per households with children under 18',labels={
                     "Food waste per person in pounds": "Food waste per person(lbs)",
                 })
dash_app.layout = html.Div([

    html.Div([
        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='my_dropdown',
            options=[
              {'label': 'Households with children under 18 years old', 'value': 'Householdswithchildrenunder18yearsold'},
              {'label': 'Racial Diversity Index', 'value': 'RacialDiversityIndex'},
              {'label': 'Population aged 65', 'value': 'Populationaged65'},
              {'label': 'Population aged 25 with a bachelors degree or higher', 'value': 'Populationaged25withabachelorsdegreeorhigher'},
              {'label': 'Population aged 25 without high school diploma', 'value': 'Populationaged25withouthighschooldiploma'},
              {'label': 'Unemployment rate', 'value': 'Unemployment rate'},
              {'label': 'Percentage Unemployment', 'value': 'PercentageUnemployment'},
              {'label': 'Poverty Rate', 'value': 'Poverty Rate'},
              {'label': 'Food waste per person in pounds', 'value': 'Food waste per person in pounds'},
              {'label': 'Median Household Income', 'value': 'Median Household Income'}
          ],
            optionHeight=35,                    
            value='Householdswithchildrenunder18yearsold',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
              
            ),                   
    
    html.Br(),
    html.Div(id='output_data'),
    html.Br(),     
    ],className='three columns'),


    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),
])


@dash_app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    dff=result
    names=column_chosen
    fig = px.scatter(dff, x=names, y='Food waste per person in pounds', template="plotly", trendline="ols")
    fig.update_layout(title={'text':names+" in relation to food waster per person",
                      'font':{'size':20}})
    return fig




if(__name__=="__main__"):
    app.run(debug=True)
    dash_app.run_server(debug=True)