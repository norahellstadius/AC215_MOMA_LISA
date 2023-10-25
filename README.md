# MOMA Lisa
### Nora Hallqvist, Anna Midgley, Sebastian Weisshaar

**Project Description:**
Our project takes a user's prompt, and generates a MoMa artwork. We finetune Stable Diffusion with the artworks currently on display in the Museum Of Modern Art (MOMA) in New York. 

### Project organization 

    ├── LICENSE
    ├── README.md
    ├── data.dvc
    ├── imgs
    │   ├── ...
    ├── reports
    │   ├── milestone2.md
    │   └── milestone3.md
    └── src
        ├── docker-compose.yml
        ├── preprocess
        │   ├── Dockerfile
        │   ├── preprocess.py
        │   └── requirements.txt
        ├── scrape
        │   ├── Dockerfile
        │   ├── Pipfile
        │   ├── Pipfile.lock
        │   └── scraper.py
        ├── secrets
        │   ├── data-service-account.json
        │   └── wandb_api_key.json
        └── train
            ├── Dockerfile
            ├── fetch_train_data.py
            ├── requirements.txt
            ├── train.sh
            └── training_setup.sh

### Code structure
* `src/preprocess/preprocess.py` : Fetches MOMA images from 'moma_scrape' GCP bucket, converts the images to png formate and annotates them by generate a text caption and uploads to 'preprocess_data' bucket.

* `src/scrape/scraper.py` : Scrape MOMA collection of artworks currently on display and store jpeg files in 'moma_scrape' GCP bucket. 

* `src/train/fetch_train_data.py` : Fetch training data from 'preprocess_data' bucket and store it for training. 

* `src/train/training_setup.sh` : Collect data and utils file for training. 

* `src/train/train.sh` : Start the fine-tuning of Stable Diffusion, **requires** to first run `training_setup.sh`

### Bucket structure 
The following is structure of our files on Google Cloud Storage. DVC tracking ensures data management, and version control over our data. The `moma_scrape` bucket contains the raw images that were scrapped from the MOMA website. 
The `preprocess_data` bucket contains the processed images, with their corresponding captions. The text captions are stored in the JSONL file. The JSONL file consists of a series of dictionaries, with each dictionary comprising two  keys: 'file_name' and 'text.' The 'file_name' key corresponds to the image's name, while the 'text' key is the image's caption. The `momalisa_model` bucket stores our model. 

    ├── dvc tracking
    │   ├── ...
    ├── moma_scrape
    │   └── imgs/
    │       ├── ...
    ├── momalisa_model
    ├── preprocess_data
    │   └── train/
    │       ├── metadata.jsonl
            ├── moma_0.png
            ├── moma_1.png
            ├── ...
        

## AC215 - Milestone 4 - MOMA Lisa

This Milestone encomposed:
1. Model deployment 
2. ML pipeline 

## Model Deployment
In this part we deploy our model on  Google Cloud's Vertex AI using a custom Docker container. It encompassed building a Docker image, pushing it to Google Cloud Registry (GCR), and deploying the model using the pushed image. Below we provide a step-by-step guide of the process we followed: 

### Prerequisites:
   - **Google Cloud SDK**: Install the Google Cloud SDK on your local machine.

   - **Credentials**: Set up your Google Cloud credentials for authentication.

   - **Role Permissions**: Need to ensure you have the necessary Google Cloud roles for Container Registry access.


### Quick Start 
Navigate to the project directory before executing any commands:

   ```bash
   cd src/deploy
   ```

### Step 1: Build and Tag Docker Images:

   Build and tag the Docker image:

   ```bash
   docker build -t gcr.io/cookthis-400019/diffusion_model:latest .
   ```

   Note the docker image follows the following name structure: gcr.io/PROJECT_ID/IMAGE_NAME:TAG


### Step 2: Push Docker Image to GCR:

   After building and tagging, push the image to Google Container Registry (GCR): 

   ```bash
   docker push gcr.io/cookthis-400019/diffusion_model:latest
   ```

### Step 3: Build a Model Using the Image on GCR:

   Use the `gcloud` CLI to build a model using the Docker image you've pushed to GCR:

   ```bash
   gcloud beta ai models upload \
   --region=us-east1 \
   --display-name=diffusion-vertexai-1 \
   --container-image-uri=gcr.io/cookthis-400019/diffusion_model:latest \
   --format="get(model)"
   ```

### Step 4: Deploy the Model via VertexAI UI:

   Deploy your built model through the VertexAI User Interface:

   - Navigate to Model Registry
   - Deploy the Model:
     1. Find and click on your model within the registry.
     2. Click on `DEPLOY AND TEST`, followed by `DEPLOY TO ENDPOINT`.
     3. To successfully deploy the model, select a single GPU with TESLA P4’s.
