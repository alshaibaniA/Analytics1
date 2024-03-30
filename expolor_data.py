import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
#import mpldatacursor
import plotly.express as px
import seaborn as sns





@st.cache_data
def load_data():
	link = "Bakery.csv"
	df = pd.read_csv(link)
	df['DateTime'] = pd.to_datetime(df['DateTime'])
	df['Date'] = df['DateTime'].dt.date
	df['Time'] = df['DateTime'].dt.time.apply(lambda x: x.strftime('%H:%M:%S'))
	df['Hour'] = df['DateTime'].dt.hour
	df['DayOfWeek'] = df['DateTime'].dt.day_name()


	st.table(df.head())
	return df
df = load_data()


def show_page():
	df = load_data()

	st.title(" Hello welcome to my dashboard")


	st.write("Select a date range to filter the data:")

	# Date range selection
	start_date = st.date_input("Start Date")
	end_date = st.date_input("End Date")

	# Filter the data based on the selected date range or use the whole dataset
	if start_date != 0 and end_date != 0:
	    df = df[
	        (df['DateTime'].dt.date >= start_date) &
	        (df['DateTime'].dt.date <= end_date)
	    ]
	else:
	    df = df.copy()

	if df.empty:
		st.write("no data available for these dates")
	else:

		st.write(
			"""

			### display pie chart

			""")
		data = df["Items"].value_counts()
		fig1, ax1 = plt.subplots()
		ax1.pie(data,labels=data.index,autopct="1.1f%%",shadow=True, startangle=90)
		ax1.axis("equal")

		st.write("""### number of data of bakery store""")
		st.pyplot(fig1)

		st.write(

				"""
					### bar chart
				"""
			)

		# Assuming you have a DataFrame named 'df' with 'Items' and 'Daypart' columns
		data = df.groupby(['Daypart', 'Items']).size().unstack()

		# Create a grouped bar chart
		fig, ax = plt.subplots()
		data.plot(kind='bar', ax=ax)

		# Set labels and title
		ax.set_xlabel('Daypart')
		ax.set_ylabel('Count')
		ax.set_title('Distribution of Items by Daypart')

		# Display the chart in Streamlit
		st.pyplot(fig)

		st.write(

				"""
					### most purchesed items in each day part
				"""
			)

		# Assuming you have a DataFrame named 'df' with columns: 'Items' and 'Daypart'
		data = df.groupby(['Daypart', 'Items']).size().reset_index(name='Count')
		max_items = data.groupby('Daypart')['Count'].idxmax()
		most_purchased_items = data.loc[max_items]

		# Create a bar chart
		fig, ax = plt.subplots()
		ax.bar(most_purchased_items['Daypart'], most_purchased_items['Items'])

		# Set labels and title
		ax.set_xlabel('Daypart')
		ax.set_ylabel('Most Purchased Item')
		ax.set_title('Most Purchased Item in Each Daypart')

		# Display the chart in Streamlit
		st.pyplot(fig)

		st.write(

				"""
					### display each item how many times it has been purchesed in each part of the day
				"""
			)

		# Assuming you have a DataFrame named 'df' with columns: 'Items' and 'Daypart'
		pivot_table = pd.pivot_table(df, index='Items', columns='Daypart', aggfunc='size', fill_value=0)

		# Display the pivot table in Streamlit
		st.write(pivot_table)

		st.write(

				"""
					### number of purchese of each item based on time
				"""
			)
		# Group DataFrame by time and calculate the count of items
		time_counts = df.groupby('Hour')['Items'].count()

		# Create a sequential chart
		fig, ax = plt.subplots()
		line=ax.plot(time_counts.index, time_counts.values)

		# Set labels and title
		ax.set_xlabel('Hour')
		ax.set_ylabel('Number of Items Purchased')
		ax.set_title('Sequential Chart of Items Purchased over Hour')

		mplcursors.cursor(line)
		#mpldatacursor.datacursor(hover=True)


		# Display the chart in Streamlit
		st.pyplot(fig)



		st.write(

				"""
					### is it working?
				"""
			)

		# Group DataFrame by hour and calculate the count of items
		hour_counts = df.groupby('Hour')['Items'].count().reset_index()

		# Create a sequential chart using Plotly
		fig = px.line(hour_counts, x='Hour', y='Items', labels={'Hour': 'Hour', 'Items': 'Number of Items Purchased'},
		              title='Sequential Chart of Items Purchased by Hour')

		# Enable hover information
		fig.update_traces(hovertemplate='Hour: %{x}<br>Number of Items Purchased: %{y}')

		# Display the chart in Streamlit
		st.plotly_chart(fig)


		st.write(

				"""
					### Lets try by days of the week?
				"""
			)

		# Group DataFrame by hour and calculate the count of items
		hour_counts = df.groupby('DayOfWeek')['Items'].count().reset_index()

		# Create a sequential chart using Plotly
		fig = px.line(hour_counts, x='DayOfWeek', y='Items', labels={'DayOfWeek': 'DayOfWeek', 'Items': 'Number of Items Purchased'},
		              title='Sequential Chart of Items Purchased by Day Of Week')

		# Enable hover information
		fig.update_traces(hovertemplate='DayOfWeek: %{x}<br>Number of Items Purchased: %{y}')

		# Display the chart in Streamlit
		st.plotly_chart(fig)


		st.write(

				"""
					### Heatmap
				"""
			)
		# Group DataFrame by day of the week and hour, and calculate the count of items
		purchases_by_time = df.groupby(['DayOfWeek', df['DateTime'].dt.hour])['Items'].count().unstack()

		# Create a heatmap
		fig, ax = plt.subplots(figsize=(10, 6))
		sns.heatmap(purchases_by_time, cmap='YlOrRd', ax=ax, annot=True, fmt='g')

		# Set labels and title
		ax.set_xlabel('Hour of the Day')
		ax.set_ylabel('Day of the Week')
		ax.set_title('Number of Purchases by Time and Day of the Week')

		# Adjust the layout to prevent cutoff of labels
		plt.tight_layout()

		# Display the chart in Streamlit
		st.pyplot(fig)




		st.write(

				"""
					### number of purchese that occur in each single day
				"""
			)
		# Assuming you have a DataFrame named 'df' with a 'Date' column
		df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

		# Group DataFrame by date and calculate the count of purchases
		daily_purchases = df.groupby(df['Date'].dt.date)['Items'].count()

		# Create a line chart
		fig, ax = plt.subplots()
		line, =ax.plot(daily_purchases.index, daily_purchases.values)

		# Set labels and title
		ax.set_xlabel('Date')
		ax.set_ylabel('Number of Purchases')
		ax.set_title('Purchases by Date')

		# Rotate x-axis labels for better readability
		plt.xticks(rotation=45)

		# Create the cursor tooltip
		mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[0]}, {sel.target[1]}"))
		# Display the chart in Streamlit
		st.pyplot(fig)


		st.write(

				"""
					### Enable cursor
				"""
			)
		# Assuming you have a DataFrame named 'df' with a 'Date' column
		df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

		# Group DataFrame by date and calculate the count of purchases
		daily_purchases = df.groupby(df['Date'].dt.date)['Items'].count().reset_index()

		# Create a line chart with hover tooltips
		fig = px.line(daily_purchases, x='Date', y='Items', labels={'Date': 'Date', 'Items': 'Number of Purchases'},
		              title='Purchases by Date')
		fig.update_xaxes(tickangle=45)

		# Enable hover tooltips
		fig.update_traces(hovertemplate='Date: %{x}<br>Number of Purchases: %{y}')

		# Display the chart in Streamlit
		st.plotly_chart(fig)

		st.experimental_rerun()
