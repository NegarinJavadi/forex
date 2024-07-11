import datetime as dt
import plotly.graph_objects as go
from pyparsing import line
from plotly.subplots import make_subplots

class CandlePlot:
#have methods to create and display candlestick plots

    def __init__(self, df, candles=True):
        self.df_plot = df.copy()
        #creates a copy of the DataFrame df and stores it in self.df_plot
        self.candles = candles
        #stores the value of the candles parameter in self.candles
        self.create_candle_fig()
        #calls the create_candle_fig method to create the initial plot

    def add_timestr(self):
    #add a formatted time string to the DataFrame
        self.df_plot['sTime']= [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") 
                        for x in self.df_plot.time]
        #creates a new column sTime in self.df_plot, containing formatted time strings based on the time column


    def create_candle_fig(self):
    #defines a method to create the candlestick plot
        self.add_timestr()
        #to add the formatted time strings to the DataFrame
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        #creates a subplot figure with secondary y-axis enabled and stores
        if self.candles == True:
            self.fig.add_trace(go.Candlestick(
                x=self.df_plot.sTime,
                open= self.df_plot.mid_o,
                high= self.df_plot.mid_h,
                low= self.df_plot.mid_l,
                close= self.df_plot.mid_c,
                line=dict(width=1), opacity=1,
                increasing_fillcolor='#24A06B',
                decreasing_fillcolor='#CC2E3C',
                increasing_line_color='#2EC886',
                decreasing_line_color='#FF3A4C'

             ))
            #adds a candlestick trace to the plot with various settings for appearance
        
    def update_layout(self, width, height, nticks):
    #defines a method to update the layout of the plot
        self.fig.update_yaxes(
            gridcolor= "#1f292f"
            )
        #updates the y-axis grid color

        self.fig.update_xaxes(
            gridcolor= "#1f292f",
            rangeslider=dict(visible=False),
            nticks=nticks
        )
        #updates the x-axis grid color, hides the range slider, and sets the number of ticks

        self.fig.update_layout(
            width=width,
            height=height,
            margin=dict(l=10, r=10, b=10, t=10),
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            font=dict(size=8, color= "#e1e1e1")
        )
        #updates various layout settings

    def add_traces(self, line_traces, is_sec=False):
    #defines a method to add line traces to the plot
        for t in line_traces:
            self.fig.add_trace(go.Scatter(
                x=self.df_plot.sTime,
                y=self.df_plot[t],
                line=dict(width=2),
                line_shape="spline",
                name=t
            ), secondary_y=is_sec)
        #adds a scatter (line) trace to the plot


    def show_plot(self,width=900, height=400, nticks=5, line_traces=[], sec_traces=[]):
    #defines a method to show the plot with customizable settings
        self.add_traces(line_traces)
        #adds primary line traces to the plot
        self.add_traces(sec_traces, is_sec=True)
        #adds secondary line traces to the plot
        self.update_layout(width,height, nticks)
        #updates the layout of the plot
        self.fig.show()
        #displays the plot