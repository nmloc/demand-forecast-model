
import pickle
from sklearn.pipeline import Pipeline
import pandas as pd
# from google.cloud import storage
import os
import functions_framework

# BUCKET_NAME = os.environ["BUCKET_NAME"]
# PICKLE_PATH = os.environ["PICKLE_PATH"]

# def read_file_from_cloud_storage(bucket_name: str, file_path: str):
#     # Create a client
#     client = storage.Client()

#     # Get the bucket
#     bucket = client.get_bucket(bucket_name)

#     # Get the blob (object) by its name
#     blob = bucket.get_blob(file_path)

#     # Read the contents of the object as bytes
#     bytes_content = blob.download_as_bytes()

#     return pickle.load(bytes_content)

# def load_cloud_model(path: str = "pet-care-b0d24.appspot.com/demand-forecast-model/v2/model_v2.pkl") -> Pipeline:
#     model = read_file_from_cloud_storage(BUCKET_NAME, path)
#     return model

def load_model(path: str = "model.pkl") -> Pipeline:
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


@functions_framework.http
def predict_http(request):
    request_json = request.get_json(silent=True)
    model = load_model()
    result = model.predict(pd.DataFrame(request_json))
    print("Result:", result)
    return result

