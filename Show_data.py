import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
#import mpldatacursor
import plotly.express as px
import seaborn as sns

def show_data(df):
	st.title("Time-based Analysis")
	st.write("Select a time for analysis:")
	# Time interval selection
	time_interval = st.selectbox("Time Interval", ["Hourly", "Daily", "Weekly", "Monthly"])

	# Perform analysis based on the selected time interval
	if time_interval == "Hourly":
		analysis_df = df.groupby(df['DateTime'].dt.hour)['TransactionNo'].count()
		xlabel = "Hour"
		title = "Hourly Sales Trend"
	elif time_interval == "Daily":
		analysis_df = df.groupby(df['DateTime'].dt.date)['TransactionNo'].count()
		xlabel = "Date"
		title = "Daily Sales Trend"
	elif time_interval == "Weekly":
		analysis_df = df.groupby(df['DateTime'].dt.isocalendar().week)['TransactionNo'].count()
		xlabel = "Week"
		title = "Weekly Sales Trend"
	elif time_interval == "Monthly":
		analysis_df = df.groupby(df['DateTime'].dt.month)['TransactionNo'].count()
		xlabel = "Month"
		title = "Monthly Sales Trend"

	# Plot the sales trend
	fig, ax = plt.subplots()
	analysis_df.plot(kind='line', ax=ax)
	#Hoover
	
	mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[0]}, {sel.target[1]}"))

	

	ax.set_xlabel(xlabel)
	ax.set_ylabel('Sales Count')
	ax.set_title(title)
	st.pyplot(fig)

