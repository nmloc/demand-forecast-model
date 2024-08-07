from datetime import datetime
import pandas as pd
import pickle
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ngminhloc/.config/gcloud/application_default_credentials.json"
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from json_to_df import JSONToDataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def clean_training_data():
		df = pd.DataFrame(pd.read_json('pet-guardian.json'))
		df = df[(df['paid'] == True)]
		df['dateRequired'] = pd.to_datetime(df['dateRequired'], format='%Y-%m-%d %H:%M:%S')
		df['year-month'] = df['dateRequired'].dt.strftime('%Y-%m')
		grouped_df = df.groupby(['year-month','itemCategory']).size().reset_index(name='count')
		grouped_df = grouped_df.sort_values(by='year-month')

		# Extract year and month as separate features
		grouped_df['year-month'] = pd.to_datetime(grouped_df['year-month'])
		grouped_df['year'] = grouped_df['year-month'].dt.year
		grouped_df['month'] = grouped_df['year-month'].dt.month
		grouped_df = grouped_df.drop(columns=['year-month'])

		return grouped_df

def trained_model():
    df = clean_training_data()

    X = df[['year', 'month', 'itemCategory']]
    y = df['count']

    preprocessor = ColumnTransformer(
        transformers=[
            ('year', OneHotEncoder(handle_unknown='ignore'), ['year']),
            ('month', OneHotEncoder(handle_unknown='ignore'), ['month']),
            ('itemCategory', OneHotEncoder(handle_unknown='ignore'), ['itemCategory'])
        ],
        remainder='passthrough'  # Keep any other columns that aren't explicitly transformed
    )

    pipeline = Pipeline(steps=[
        ('json_to_df', JSONToDataFrame()),
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    pipeline.fit(X, y)

    return pipeline
    
def export():
    with open('model_v2.pkl', 'wb') as file:
        pickle.dump(trained_model(), file)

def generate_future_data(future_periods, category):
    future_dates = pd.date_range(start=datetime.now() + pd.DateOffset(months=1), periods=future_periods, freq='M')

    # Create a DataFrame for future predictions
    future_df = pd.DataFrame({
        'year': future_dates.year,
        'month': future_dates.month,
        'itemCategory': [category] * future_periods
    })

    return future_df

def predict(future_periods, category):
    model = trained_model()
    future_data = generate_future_data(future_periods, category)
    print(future_data.to_json(orient='records'))
    y_pred_future = model.predict(future_data)

    print(y_pred_future)
    # return future_data, y_pred_future

def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

    
# Main function
if __name__ == "__main__":
    # json_input = [{"year":2024,"month":6,"itemCategory":"Grooming"},{"year":2024,"month":7,"itemCategory":"Grooming"},{"year":2024,"month":8,"itemCategory":"Grooming"},{"year":2024,"month":9,"itemCategory":"Grooming"},{"year":2024,"month":10,"itemCategory":"Grooming"},{"year":2024,"month":11,"itemCategory":"Grooming"}]
    # result = trained_model().predict(json_input)
    # print(result)
    # print(trained_model().predict([{"year": 2024, "month": 12, "itemCategory": "Grooming"}]))
    trained_model()