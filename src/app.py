# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import numpy as np # only used here to generate random color codes in plotting (see below)
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
import data_processing
#TODO: add enabled .svg save / .png optionally


app = Dash(__name__)

# -------------------------------------------------------------------------------------------- #
# ---------------------------------------- DATA PLOTTING ------------------------------------- #

# your data source(s) instead
df_no_group = data_processing.df
df_all_groups = data_processing.df_gb
df_each_day_dict = data_processing.df_dispatched_in_dict

# VERSION WITH PLOTLY GRAPH OBJECTS -----------------------------------------------------
# generate fixed chosen colors, stored in an array
my_color_1 = ('rgba('+str(220)+','+str(115)+','+str(69)) # dark salmon
my_color_2 = ('rgba('+str(74)+','+str(219)+','+str(154)) # light green
my_color_3 = ('rgba('+str(217)+','+str(60)+','+str(225)) # magenta-ish
my_color = [my_color_1, my_color_2, my_color_3]



# Most memory efficient: using groups from one same df
fig = go.Figure()
for i, (day, group) in enumerate(df_all_groups):
    # if replacing with random color generator for n curves,
    # then replace: for i, (day, group)... enumerate(...)
    # with: for day, group in df_all_groups
    
    # other option: generate colors randomly when adding the trace
    '''
    my_color = ('rgba('+str(np.random.randint(0, high = 256))+','+
                str(np.random.randint(0, high = 256))+','+
                str(np.random.randint(0, high = 256)))
    '''
    fig.add_trace(go.Scatter(x = group['time_pdobj'],
                             y = group[data_processing.SOME_QTY_FIELD],
                             mode="lines+markers",
                             # remove [i] if my_color is randomly generated
                            marker={'color':my_color[i]+',1)'}, # 1 = full opacity,
                            line={"color":my_color[i]+',0.5)'}, # 0.5 = 50% opaque
                            name = str(day)))
fig.update_traces(marker_size = 4)
fig.update_layout(title = "Your graph title here",
                  legend_title_text = "Your legend title here",
                  height = 600,
                  xaxis_tickformat = '%H:%M:%S') # workaround to get rid of Jan 1, 1900
fig.update_xaxes(title_text = "Your x-axis title here", 
                 rangeslider_visible=True,
                 range=[datetime(1900, 1, 1, 0, 0), datetime(1900, 1, 2, 0, 0)])
fig.update_yaxes(title_text = "Your y-axis title here",
                 tickprefix = "$") # if qty = prices, for instance

# (SIMPLER) VERSION WITH PLOTLY EXPRESS -------------------------------------------------
# Seems a little limited in options to customize the graphs further
# However, good news: most update_* and add_* methods seem to remain functional
fig_easy = px.line(df_no_group, x="time_pdobj", y=data_processing.SOME_QTY_FIELD, color="date")
# marker seems unavailable with express?
fig_easy.update_layout(title = "Your graph title here",
                  legend_title_text = "Your legend title here",
                  xaxis_tickformat = '%H:%M:%S') # workaround to get rid of Jan 1, 1900
fig_easy.update_xaxes(title_text = "Your x-axis title here", 
                 rangeslider_visible=True, # no data preview in the slider! :( 
                 range=[datetime(1900, 1, 1, 0, 0), datetime(1900, 1, 2, 0, 0)])
fig_easy.update_yaxes(title_text = "Your y-axis title here",
                 tickprefix = "$") # if qty = prices, for instance




# -------------------------------------------------------------------------------------------- #
# ---------------------------------------- APP LAYOUT ---------------------------------------- #
app.layout = html.Div(children=[
    
    html.Div([
    
    html.Div(
        className="app-header",
        children=[
            html.Div("A simple Dash analytical app template", className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H3('Overview'),
            html.Div('''
                This demo file shows both how to lay out several plots
                in a Dash app, and also provide simple styling to the app layout.
                For example, this can be the text where you explain 
                the concept of your analytical app for your data science project.
            ''')
        ])
    ),
        html.H2(children='Example overlaid line/scatter plots with some daily quantity'),
        
        # elements for overlay plots
        # the master one, done with graph_objects
        html.Div(children='''
            Explain some stuff here. For example: This plot corresponds to the rendering 
            of the code of the '# VERSION WITH PLOTLY GRAPH OBJECTS' section above. 
            In this plot, I intend to show how you can use plotly.graph_objects ('go'), 
            to display your data with both lines + markers, added a '$' on y-axis labels, 
            great colours imo (that you can randomize if you're not satisfied with these!), 
            on an x-axis representing pandas' datetime data (here, time). 
            For this graph and the graph right below, I had to reformat the x-axis to %H%M%S 
            (hour-minut-seconds) so that the 'January 1900' from default pd.to_datetime() method 
            disappears. In my case, using pd.to_datetime.dt.time "at the source", in the df, 
            messed with the axes. Hence this workaround.
            Each series is a day, that you can select/unselect by clicking on the series name 
            in the legend. Finally, I updated the height in fig.update_layout() to 600px, 
            so that you see how to make a graph look like the "main one".
            Also, the range slider helps you zoom in/out horizontally on a certain time range. 
            When used with plotly.graph_objects, the preview of the data is even visible 
            in the range slider itself! 
            Don't hesitate to fiddle with the settings, replace the different titles as you wish.
        '''),
        dcc.Graph(
            id='example-overlaid-scatter-plots', 
            figure=fig
            ),
        # the easier overlay plot, done with plotly express
        html.Div(children='''
            Explain some other stuff here. For example: We are still in the 
            overlaid plots section here, but this time the plot was generated with 
            plotly.express ('px'). The code that renders it is in the above  
            '# (SIMPLER) VERSION WITH PLOTLY EXPRESS' section. 
            Notice that I did not add any customization to the lines, they show no markers. 
            I noticed that without markers, the data sliding with the range slider 
            is less lagging than with above graph (at least when displayed in Chrome). 
            Also the colours are randomly generated, I did not specify them. 
            plotly.express will render random colours that are really contrasting 
            against one another. 
            Notice how the range slider does not show the preview of the data this time... 
            '''),
        dcc.Graph(
            id='example-overlaid-scatter-plots-easy', 
            figure=fig_easy,
            ),
    ]),

    # New Div for indidual plots in the new 'row' of the page
    html.Div([
        html.H2(children='Example single scatter plots with some daily quantity, with drop-down to select date.'),
        html.Div(children='''
        Explain some different stuff here. For example: I also wanted to show my data 
        from a different angle. I wanted to allow the user to scrutinize the data, 
        with their attention focused on one single day, that they can select from the 
        interactive drop-down 'Select date: ' below. Here, the data does not seem to show any 
        particular pattern, because this is dummy data generated randomly with my JS 
        randomDBGenerator. This plot is also created with plotly express!'''),
        dcc.Graph(id='example-single-scatter-plots'),
        html.P("Select date: "),
        dcc.Dropdown(
            id="ticker",
            options=list(df_each_day_dict.keys()),
            value='2012-01-01', # default value displayed when landing on the app
            clearable=False,
        ),
    ]),
])

# INTERACTIVE DROP-DOWN FOR SINGLE DAILY PLOTS DISPLAY ---------------------------------
@app.callback(
    Output("example-single-scatter-plots", "figure"),
    Input("ticker", "value"))

#TODO: find a way to re use same df as above in 
# filtering/grouping (df[df["date"] == ticker] does not seem to work for now)*
# for memory-efficiency
# to check the type of "ticker"
def display_day_series(ticker):
    fig = px.scatter(df_each_day_dict[ticker], x="time", y=data_processing.SOME_QTY_FIELD)
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)