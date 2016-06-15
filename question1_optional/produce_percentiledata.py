import wget
import numpy as np
import pandas as pd
import time as time
import math
import os
from bokeh.plotting import output_file, show, save
from bokeh.plotting import Figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBox, HBox, Select
from bokeh.palettes import Blues4
from bokeh.embed import file_html
import argparse
from extract_data_from_csv import extract_data_from_csv

def percentile_Calculation(MinTemp,MaxTemp,percent):
    MinTempPercentile = []
    MaxTempPercentile = []
    percent = percent/100
    for index in range(len(MinTemp)):
        MinTempPercentile.append(MinTemp[index]+(MinTemp[index]*percent))
        MaxTempPercentile.append(MaxTemp[index]-(MaxTemp[index]*percent))
    return MinTempPercentile,MaxTempPercentile

def make_plot(source,AverageTemp,Parcentile_5_Min,Parcentile_5_Max,Parcentile_25_Min,Parcentile_25_Max,MinTemp,MaxTemp,plotDate,cityName):
    plot = Figure(title='Optional Task # 1 : Growing Degree-day for '+cityName, x_axis_type="datetime", plot_width=1000, title_text_font_size='12pt', tools="", toolbar_location=None)
    colors = Blues4[0:3]
    
    plot.circle(MaxTemp,MinTemp, alpha=0.9, color="#66ff33", fill_alpha=0.2, size=10,source=source,legend ='2015')
    plot.quad(top=Parcentile_5_Max, bottom=Parcentile_5_Min, left='left',right='right',
              source=source,color="#e67300", legend="Percentile 5-95")
    plot.quad(top=Parcentile_25_Max, bottom=Parcentile_25_Min,left='left',right='right',
              source=source,color="#66ccff",legend="percentile 25-75")
    plot.line(plotDate,AverageTemp,source=source,line_color='Red', line_width=0.75, legend='AverageTemp')

    plot.border_fill_color = "whitesmoke"
    plot.xaxis.axis_label = "Months"
    plot.yaxis.axis_label = "Temperature (C)"
    plot.axis.major_label_text_font_size = "10pt"
    plot.axis.axis_label_text_font_size = "12pt"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0, bounds=None)
    plot.grid.grid_line_alpha = 0.3
    plot.grid[0].ticker.desired_num_ticks = 12
    return plot

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", dest="stationId", nargs = '*', help="Please provide a list of station Id.")
    parser.add_argument("-ct", dest="cityName", nargs = '*', help="Please provide a list of city names corresponding to stations.")
    args = parser.parse_args()
    CurrentPath = os.getcwd()
    for i in range(len(args.stationId)):
        FilePath= (CurrentPath+'/DataFiles/GDD_Data_'+args.cityName[i]+'.csv')
        Data, Date, MaxTemp, MinTemp = extract_data_from_csv(FilePath)
        Data['date'] = pd.to_datetime(Date)
        Data['left'] = Data.date - pd.DateOffset(days=0.5)
        Data['right'] = Data.date + pd.DateOffset(days=0.5)
        PlotDate =[]
        plotDate = Data['right']
        Data = Data.set_index(['date'])
        Data.sort_index(inplace=True)
        source = ColumnDataSource(data=Data)
        AverageTemp = []
        for index in range(len(MinTemp)):
            Average=(MinTemp[index]+MaxTemp[index])/2
            AverageTemp.append(Average)
    
        percent = 5
        Min_5_95, Max_5_95 =percentile_Calculation(MinTemp,MaxTemp,percent)
        percent = 25
        Min_25_75, Max_25_75 =percentile_Calculation(MinTemp,MaxTemp,percent)

        plot = make_plot(source,AverageTemp,Min_5_95,Max_5_95,Min_25_75,Max_25_75, MinTemp,MaxTemp,plotDate,args.cityName[i])
        output_file("./Plots/Op1_"+args.cityName[i]+".html", title="Optional Task # 1 ("+args.cityName[i]+")")
        save(plot)

if __name__ == '__main__':
Main()
