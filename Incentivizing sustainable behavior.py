import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

# Load the user's spending data
spending_data = pd.read_csv('user_spending.csv')

# Clean the data
spending_data = spending_data.dropna()
spending_data['Date'] = pd.to_datetime(spending_data['Date'], format='%Y-%m-%d')

# Use KMeans clustering to identify patterns in the user's spending
scaler = MinMaxScaler()
spending_data['Amount_scaled'] = scaler.fit_transform(spending_data[['Amount']])
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(spending_data[['Amount_scaled']])
spending_data['Cluster'] = kmeans.labels_

# Compute the average spending for each cluster
cluster_means = spending_data.groupby('Cluster').mean()

# Identify the cluster with the highest average spending
high_spending_cluster = cluster_means['Amount'].idxmax()

# Provide recommendations for sustainable behavior based on the high-spending cluster
if high_spending_cluster == 0:
    print("You might want to consider reducing your spending on entertainment.")
elif high_spending_cluster == 1:
    print("You might want to consider reducing your spending on dining out.")
else:
    print("You might want to consider reducing your spending on travel.")

# Use linear regression to predict future spending behavior
X = spending_data[['Date']]
y = spending_data['Amount_scaled']

model = LinearRegression()
model.fit(X, y)

# Predict future spending for the next month
next_month = pd.date_range(start='2023-05-01', end='2023-05-31')
next_month_df = pd.DataFrame({'Date': next_month})
next_month_df['Month'] = next_month_df['Date'].dt.month
next_month_df['Year'] = next_month_df['Date'].dt.year
next_month_df['Days_in_month'] = next_month_df['Date'].dt.daysinmonth
next_month_df['Weekday'] = next_month_df['Date'].dt.weekday
next_month_df['Is_weekend'] = np.where(next_month_df['Weekday'] < 5, 0, 1)
next_month_df = next_month_df.drop('Date', axis=1)

predicted_spending_scaled = model.predict(next_month_df)
predicted_spending = scaler.inverse_transform(predicted_spending_scaled)

# Provide personalized advice based on the predicted spending
if predicted_spending.mean() > spending_data['Amount'].mean():
    print("You might want to consider creating a budget to manage your spending.")
else:
    print("Your spending is within a healthy range.")