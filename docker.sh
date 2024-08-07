PROJECT_ID=pet-care-b0d24
REGION=us-central1
REPOSITORY=demand-forecast

# # Create repository in the artifact registry
# gcloud beta artifacts repositories create $PROJECT_ID/$REPOSITORY \
#   --repository-format=docker \
#   --location=$REGION

# Configure Docker
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build the Docker image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/v2 .

# Push
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/v2