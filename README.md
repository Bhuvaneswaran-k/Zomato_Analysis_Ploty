# Zomato_dataset_analaysis_Ploty_dashboard

# Installation
                                      pip install jupyter_dash 
                                      pip install dash_bootstrap_components
                                      pip install pandas
                                      pip install ploty
          
# Ploty
plotly.py, colloquially referred to as Plotly, is an interactive, open-source, and browser-based graphing library. It offers Python-based charting, powered by plotly. js. The library ships with over 30 chart types, including scientific charts, 3D graphs, statistical charts, SVG maps, financial charts, and more

The main plus point of plotly is its interactive nature and of course visual quality. Plotly is in great demand rather than other libraries like Matplotlib and Seaborn. Plotly provides a list of charts having animations in 1D, 2D, and 3D too for more details of charts check  

  # Importation Part
                                      import pandas as pd
                                      from dash import Dash, html, Input, Output, dcc
                                      import plotly.express as px
                                      import dash_bootstrap_components as dbc
                                      import plotly.graph_objects as go
                                      from plotly.subplots import make_subplots
                                      import requests
