import pandas as pd
from dash import Dash, html, Input, Output, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

#data set loading
url = 'https://github.com/Bhuvaneswaran-k/Zomato_Analysis_Ploty/blob/main/zomato.csv?raw=True'
zomato_df = pd.read_csv(url,index_col=0)
url1='https://github.com/Bhuvaneswaran-k/Zomato_Analysis_Ploty/blob/main/Country-Code.xlsx%20-%20Sheet1.csv?raw=True'
contry_code_df=pd.read_csv(url1,index_col=0)

#creating dash
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

#conversion to INR

inr_list = []
for j in contry_code_df["Currency Code"]:
  api_url = f'https://api.exchangerate.host/convert?from={j}&to=INR'
  response = requests.get(api_url)
  data = response.json()
  result= data["result"]
  inr_list.append(round(result,2))

contry_code_df["inr_list"]=inr_list

#Merging two datasets on basis of Country code
final_df= pd.merge(zomato_df,contry_code_df, on = "Country Code")

final_df["Average Cost in INR"] = final_df["inr_list"]*final_df["Average Cost for two"]

country_list= final_df.Country.unique()
#colour code for text
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#creating Page Layout
app.layout = html.Div(
    html.Div(children=[
        html.H1("Bhuvi's Dashboard for Zomato Dataset Analysis",style={
            'textAlign': 'center',
            'color': colors['text']}),
        html.Label("Select Country to see analysis about shops in cities : "),
        dcc.Dropdown(
            id="Country_dropdown",
            options=[{"label": x, "value": x} for x in country_list],
            placeholder="Select a Country",
        ),
        html.Div([
        dcc.Graph(id="Total_Amount_Chart", className="bg-light border"),

        dcc.Graph(id="No_Shop_Chart", className="bg-light border"),
],className="hstack gap-2"),

        html.Label("Select a City to Analsis Cuisines"),
        dcc.Dropdown(
            id="city_dropdown",
            placeholder="Select a City"
        ),
        html.H3("Favourite Type of dish ",style={'textAlign': 'center'}),
        dcc.Graph(id="favorite_type_of_dish"),
        html.H3("Cusines by means of Price",style={'textAlign': 'center'}),
        dcc.Graph(id="City_costly_cus-chart"),
        html.H3("Cusines by means of Rating",style={'textAlign': 'center'}),
        dcc.Graph(id="City_rating-chart"),
        html.H3("Percentage of shops have online delivery in selected city",style={'textAlign': 'center'}),
        dcc.Graph(id="City_delivery-chart"),
        html.H3("Percentage of shops have Dine inn in selected city",style={'textAlign': 'center'}),
        dcc.Graph(id="din-in-chart"),
        html.Label("Select City to compare"),
        dcc.Dropdown(
            id="citydropdown_1",
            value="Bangalore",
            multi=True
        ),
        html.H3("Comparison chart on Amount Spend online orders",style={'textAlign': 'center'}),
        dcc.Graph(id="multi-chart_1"),
        html.H3("Comparison chart on Dine Inn",style={'textAlign': 'center'}),
        dcc.Graph(id="multi-chart_2"),
        html.H3("High living cost vs Low living Cost",style={'textAlign': 'center'}),
        dcc.Graph(id="multi-chart_3")
    ]
    )
)

#call Back and its Function
@app.callback(
    Output("Total_Amount_Chart", "figure"),
    [Input("Country_dropdown", "value")])
def update_bar_chart(Country):
    # comparision chart of cities
    Selected_country = final_df[final_df["Country"] == Country]
    city_cost = Selected_country.groupby("City")["Average Cost in INR"].sum()
    city_cost = pd.DataFrame(city_cost)
    city_cost.rename(columns={"Average Cost in INR": "Amount Spent"},inplace=True)

    fig = px.bar(city_cost, y="Amount Spent",color_discrete_sequence=["magenta"])

    fig.update_layout(
        title=(f"Total Amount Spend by Cities in {Country}"),
        xaxis_title=(f"Cities in {Country}"),
        yaxis_title="Rupees"
    )

    return fig


@app.callback(
    Output("No_Shop_Chart", "figure"),
    [Input("Country_dropdown", "value")])
def update_bar_chart(Country):
    Selected_country = final_df[final_df["Country"] == Country]
    city = Selected_country.groupby("City")["Country"].count()
    city = pd.DataFrame(city)
    city.rename(columns={"Country": "Shops"}, inplace=True)

    fig = px.bar(city, y="Shops",color_discrete_sequence=["green"])

    fig.update_layout(
        title=(f"Total Number of Shops in the Cities of {Country}"),
        xaxis_title=(f"Cities in {Country}"),
        yaxis_title="Number of shops", )

    return fig


@app.callback(
    Output("city_dropdown", "options"),
    Output("citydropdown_1", "options"),
    [Input("Country_dropdown", "value")])
# Select city dropdown
def update_city_dropdown(Country):
    Selected_country = final_df[final_df["Country"] == Country]
    return [{"label": x, "value": x} for x in Selected_country.City.unique()], [{"label": x, "value": x} for x in
                                                                                  Selected_country.City.unique()]

# pie chart1 - by means of favorite
@app.callback(
    Output("favorite_type_of_dish", "figure"),
    Input("city_dropdown", "value"),
    prevent_initial_call=True)

def update_fav_cus(input_value):

    Selected_city = final_df[final_df["City"] == input_value]
    fig = px.pie(Selected_city, names="Cuisines")
    fig
    return fig


# pie chart 2 - by means of price
@app.callback(
    Output("City_costly_cus-chart", "figure"),
    Input("city_dropdown", "value"),
    prevent_initial_call=True)
def update_fav_cus(input_value):
    #  return f'input_value:{input_value.upper()}'
    Selected_city = final_df[final_df["City"] == input_value]

    fig = px.pie(Selected_city, names="Cuisines", values="Average Cost in INR")
    fig
    return fig


# pie chart 3 - by means of rating,votes,price
@app.callback(
    Output("City_rating-chart", "figure"),
    Input("city_dropdown", "value"),
    prevent_initial_call=True)
def update_fav_cus(input_value):
    Selected_city = final_df[final_df["City"] == input_value]
    fig = px.scatter(Selected_city, x="Cuisines", y="Aggregate rating",
                     size="Votes", hover_name="Restaurant Name", color="Average Cost in INR")

    return fig


@app.callback(
    Output("City_delivery-chart", "figure"),
    Input("city_dropdown", "value"),
    prevent_initial_call=True)
def update_fav_cus(input_value):
    Selected_city = final_df[final_df["City"] == input_value]
    fig = px.pie(Selected_city, names="Has Online delivery", )
    fig
    return fig
@app.callback(
   Output("din-in-chart", "figure"),
   Input("city_dropdown", "value"),
  prevent_initial_call=True)

def update_fav_cus(input_value):
  Selected_city = final_df[final_df["City"]== input_value]
  fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
  fig.add_trace(go.Pie(labels=Selected_city["Has Table booking"]),
                1, 1)
  fig.add_trace(go.Pie(labels=Selected_city["Has Online delivery"]),
                1, 2)

  fig.update_traces(hole=.4)


  fig.update_layout(
      title_text="Dine inn vs Online Delivery")
  return fig


@app.callback(
   Output("multi-chart_1", "figure"),
   Input("citydropdown_1", "value"),
   prevent_initial_call=True
 )

def update_comp_chart_1(val_chosen):

  Selected_city = final_df[final_df["City"].isin(val_chosen)]
  Data = Selected_city[Selected_city["Has Online delivery"]=="Yes"]
  a = Data.groupby("City")["Average Cost in INR"].sum()
  a = pd.DataFrame(a)
  a.rename(columns={"Average Cost in INR": "Total Amount Spent"},inplace = True)


  fig = px.bar(a, y="Total Amount Spent",  color_discrete_sequence=["goldenrod", "magenta"])
  fig

  return fig

@app.callback(
   Output("multi-chart_2", "figure"),
   Input("citydropdown_1", "value"),
   prevent_initial_call=True
 )

def update_comp_chart_2(val_chosen):

  Selected_city = final_df[final_df["City"].isin(val_chosen)]
  Data = Selected_city[Selected_city["Has Table booking"]=="Yes"]
  a = Data.groupby("City")["Average Cost in INR"].sum()
  a = pd.DataFrame(a)
  a.rename(columns={"Average Cost in INR": "Total Amount Spent"},inplace = True)


  fig = px.bar(a, y="Total Amount Spent",color_discrete_sequence=["red"])
  fig

  return fig

@app.callback(
   Output("multi-chart_3", "figure"),
   Input("citydropdown_1", "value"),
   prevent_initial_call=True
 )

def update_comp_chart_3(val_chosen):
  Selected_city = final_df[final_df["City"].isin(val_chosen)]
  Selected_city.rename(columns={"Average Cost in INR": "Cost of a dish"},inplace = True)

  fig = px.box(Selected_city, y="Cost of a dish",x = "City")

  fig
  return fig
#running the ploty server in localhost port =8501
app.run_server(port=8501)
