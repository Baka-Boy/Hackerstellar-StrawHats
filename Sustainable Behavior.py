import pandas as pd
import numpy as np
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from fcmeans import FCM
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import silhouette_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor

# Load the user's spending data
spending_data = pd.read_csv('spending.csv')

# Clean the data
spending_data = spending_data.dropna()
spending_data['date'] = pd.to_datetime(spending_data['date'], format="%d-%m-%Y")

# Preprocess the data
scaler = MinMaxScaler()
spending_data_scaled = scaler.fit_transform(spending_data[['amount']])

# Choose the number of clusters
n_clusters = 3
cluster_scores = []
for n in range(2, 10):
    fcm = FCM(n_clusters=n, m=2)
    fcm.fit(spending_data_scaled)
    cluster_scores.append(silhouette_score(spending_data_scaled, fcm.u.argmax(axis=1)))
n_clusters = np.argmax(cluster_scores) + 2

# Apply FCM clustering
fcm = FCM(n_clusters=n_clusters, m=2)
fcm.fit(spending_data_scaled)
spending_data['Cluster'] = fcm.u.argmax(axis=1)

# Compute the average spending for each cluster
cluster_means = spending_data.groupby('Cluster').mean()

# Identify the cluster with the highest average spending
high_spending_cluster = cluster_means['amount'].idxmax()

# Provide recommendations for sustainable behavior based on the high-spending cluster
if high_spending_cluster == 0:
    print("You might want to consider reducing your spending on entertainment.")
elif high_spending_cluster == 1:
    print("You might want to consider reducing your spending on food.")
elif high_spending_cluster == 2:
    print("You might want to keep yourself healthy.")
elif high_spending_cluster == 3:
    print("You might want to consider reducing your spending on traveling.")
elif high_spending_cluster == 4:
    print("You might want to consider reducing your spending on utlities.")
else:
    print("You might want to consider reducing your spending on daily needs.")


# Preprocess data
spending_data['date'] = pd.to_datetime(spending_data['date'])
spending_data['month'] = spending_data['date'].dt.month
spending_data['weekday'] = spending_data['date'].dt.weekday
spending_data['is_weekend'] = spending_data['weekday'] >= 5
spending_data['days_in_month'] = spending_data['date'].dt.days_in_month
spending_data['category'] = pd.Categorical(spending_data['category'], categories=['Food', 'Travelling', 'Entertainment','Utilities','Healthcare','Dailyneeds'], ordered=True)
spending_data['category_code'] = spending_data['category'].cat.codes

# Feature selection
features = ['days_in_month', 'is_weekend', 'month', 'weekday', 'category_code']
X = spending_data[features]
y = spending_data['amount']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train model
model = AdaBoostRegressor()
model.fit(X_train, y_train)

# Predict next month's spending
next_month_start_date = spending_data['date'].max() + pd.DateOffset(days=1)
next_month_end_date = next_month_start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
next_month_dates = pd.date_range(next_month_start_date, next_month_end_date, freq='D')
next_month_df = pd.DataFrame({'date': next_month_dates})
next_month_df['month'] = next_month_df['date'].dt.month
next_month_df['weekday'] = next_month_df['date'].dt.weekday
next_month_df['is_weekend'] = next_month_df['weekday'] >= 5
next_month_df['days_in_month'] = next_month_df['date'].dt.days_in_month
next_month_df['category_code'] = 0  # Assume food category
next_month_spending = model.predict(next_month_df[features])
predicted_spending = np.sum(next_month_spending)
print(f"Your predicted spending for next month is: ${predicted_spending:.2f}")
if predicted_spending.mean() > spending_data['amount'].mean():
    print("You might want to consider reducing your spending.")
else:
    print("Your spending is within a healthy range.")

print(next_month_start_date)
print(next_month_end_date)


# # Train model
# ab = AdaBoostRegressor()
# ab.fit(X_train, y_train)

# # Make predictions
# y_pred = ab.predict(X_test)

# # Evaluate the model
# score = ab.score(X_test, y_test)

# # Print the MSE
# print("Mean squared error: ", score)