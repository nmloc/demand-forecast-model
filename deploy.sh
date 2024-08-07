PROJECT_ID=pet-care-b0d24
BUCKET_NAME="${PROJECT_ID}.appspot.com"
MODEL_NAME=demand_forecast
REGION=us-central1
VERSION='v'`date '+%Y%m%d_%H%M%S'`
MODEL_PATH=gs://$BUCKET_NAME/demand-forecast-model
PACKAGE_PATH=gs://$BUCKET_NAME/models/$VERSION/package/black_friday_forecast-0.0.1.tar.gz

# # Package solution
# python setup.py sdist

# # Upload code to GCS
# gsutil cp ./dist/black_friday_forecast-0.0.1.tar.gz $PACKAGE_PATH

# # Upload model to GCS
# gsutil cp ./models/model.joblib $MODEL_PATH/model.joblib

# Create model if it doesn't exist
gcloud ai-platform models create $MODEL_NAME --regions $REGION --project $PROJECT_ID

# Create a version
gcloud ai-platform versions create $VERSION \
  --model $MODEL_NAME \
  --origin $MODEL_PATH \
  --runtime-version 2.11 \
  --python-version 3.7 \
  --framework SCIKIT_LEARN \
  --project $PROJECT_ID