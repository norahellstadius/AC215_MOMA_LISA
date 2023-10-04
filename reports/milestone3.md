# What's Cookin'
### Nora Hallqvist, Anna Midgley, Sebastian Weisshaar

## Milestone 3

### Experiment Tracking
- show output from W&B page

### Severless training
- show output from GCP console
- show commands for how to run severless trianing instances from code
- mention buckets name, and what type of file model saved as 


Our model training is run in a container that contains the training scripts. The 
input to the model is processed data from a GCP bucket, and the outputted trained model
has its artifacts saved to a new GCP bucket. The container is built from `src/train/DockerFile`,
using `python:3.8-slim-buster` as the base image, and setting environment variables to ensure
that the container can connect to GCS. The container can be built, or pulled, using the respective commands
```
docker build -t train . 
docker pull amidgley/train:2.0
```
To run the docker container, use `docker run -t amidgley/train:2.0`


### Code Structure
- data processing
- notebooks