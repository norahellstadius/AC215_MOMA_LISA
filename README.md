# MOMA Lisa
### Nora Hallqvist, Anna Midgley, Sebastian Weisshaar

**Project Description:**
Our project takes a user's prompt for two points, and generates a continuous series MoMa artworks transitioning between them.
We achieve this by transversing through the latent space, creating intermediate points between the two given points, from which we can decode 
and generate images from. The images are then used to produce a gif, which is displayed to the user.

**Project Journey:**
This is not the first topic we have investigated in this project. Previously, we were hoping to use image and generated caption pairs, to fine-tune a stable diffusion model on MoMA artworks. We set up severless training, that utilized images & captions stored in a GCP bucket with WandB used to track
model training. However, we realized that the model was already to good and consequently we were unable to teach the model anything. For this reason, we decided to pivot to a different idea. We experimented with instead trying to learn specific lesser known artists styles. Unfortunately we realized that for any artist that had satisfactory set of artworks available, the model already knew the style, and again found ourselves unable to teach the model anything. Thus, we have switched to our current topic. It should be noted that the following folders of work in `src` are from previous project
ideas and not applicable to our current idea: `train`, `preprocess`, `scrape`, `data`. 

### Project organization 

    ├── LICENSE
    ├── README.md
    ├── data.dvc
    ├── imgs
    │   └── ...
    ├── reports
    │   └── ...
    └── src
        ├── docker-compose.yml
        ├── preprocess
        │   └── ...
        ├── scrape
        │   └── ...
        ├── secrets
        │   └── ...
        ├── train
        │   └── ...
        ├── deploy_model
        │   └── ...
        ├── workflow
        │   └── ...
        ├── frontend-simple
        │   ├── imgs
        │   ├── docker-shell.sh
        │   ├── Dockerfile
        │   └── index.html
        ├── api-service
        │   ├── api
        │   │   ├── model.py
        │   │   └── service.py
        │   ├── docker-entrypoint.sh
        │   ├── docker-shell.sh
        │   ├── Dockerfile
        │   ├── Pipfile
        │   └── requirements.txt
        └── deployment
            └── nginx-conf/nginx
                └── nginx.conf
            ├── deploy-create-instance.yml
            ├── deploy-docker-images.yml
            ├── deploy-provision-instance.yml
            ├── deploy-setup-containers.yml
            ├── deploy-setup-webserver.yml
            ├── docker-entrypoint.sh 
            ├── docker-shell.sh
            ├── Dockerfil
            └── inventory.yml

### Code structure
We have focused on providing a code structure description for the section of work we have added this milestone.

**Frontend:**
* `src/frontend-simple/docker-shell.sh` : This script is used to build and launch the container for the frontend.
* `src/frontend-simple/Dockerfile` : This file is used to specify the frontend container image.
* `src/frontend-simple/index.html` : This file is the html file for the frontend. It contains the html code for the website.

**API Service/Backend:**
* `src/api-service/api/model.py` : This file make predictions from the deployed model.
* `src/api-service/api/service.py` : This file is used to create the API service, and connect to the deployed model and call the predict function.
* `src/api-service/docker-entrypoint.sh` : This script is used to define the entrypoint for the backend container.
* `src/api-service/docker-shell.sh` : This script is used to build and launch the container for the API service container.
* `src/api-service/Dockerfile` : This file is used to specify the API service container image.
* `src/api-service/Pipfile` and `src/api-service/requirements.txt` : These files are used to specify the dependencies for the API service.

**Deployment:**
* `src/deployment/deploy-create-instance.yml` : This file is used to create a VM instance on GCP.
* `src/deployment/deploy-docker-images.yml` : This file is used to build and push the docker images to GCR for both the frontend and backend containers.
* `src/deployment/deploy-provision-instance.yml` : This file is used to provision the VM instance.
* `src/deployment/deploy-setup-containers.yml` : This file is used to set up the containers on the VM instance, pulling them from the container registry.
* `src/deployment/deploy-setup-webserver.yml` : This file is used to set up the webserver on the VM instance, which uses nginx to connect the frontend & backend containers.
* `src/deployment/docker-entrypoint.sh` : This script is used to define the entrypoint for the deployment container.
* `src/deployment/docker-shell.sh` : This script is used to build and launch the container for the deployment container, from which the ansible playbooks can be called.
* `src/deployment/Dockerfile` : This file is used to specify the deployment container image.
* `src/deployment/inventory.yml` : This file is used to specify the VM instance, and the containers that will be run on it.

### Bucket structure 
The following is our current structure of files on Google Cloud Storage.

    ├── saved_predictions
    │   └── instance_id
    │       ├── unique_name.gif
            ├── ...

The following is the previous structure of our files. DVC tracking was used to ensure data management, and version control over our data. The `moma_scrape` bucket contained the raw images that were scrapped from the MOMA website. 
The `preprocess_data` bucket contained the processed images, with their corresponding captions. The text captions were stored in the JSONL file. The JSONL file consisted of a series of dictionaries, with each dictionary comprising two  keys: 'file_name' and 'text.' The 'file_name' key corresponds to the image's name, while the 'text' key is the image's caption. The `momalisa_model` bucket stored our model. 

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
        

## AC215 - Milestone 6 - MOMA Lisa

## Kubernetes Setup and Deployment
For scaling purposes we set up Kubernetes. The following commands are used to deploy our application:

1. Build the deployment container: `sh docker-shell.sh`
2. Create and deploy the cluster: `ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present`
3. Copy the `nginx_ingress_ip` from the terminal from the create cluster command
4. Visit the website: `http://<INGRESS IP>.sslip.io`

To delete the cluster, run the following command: `ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=absent`

Check out these screenshots showcasing a successfully configured Kubernetes setup:

## Kubernetes Cluster Screenshots

<figure>
    <img src="./imgs/cluster.jpeg" height="200" />
    <figcaption>Running Cluster </figcaption>
</figure>


<figure>
    <img src="./imgs/workloads.jpeg" height="200" />
    <figcaption>Workloads (containers) in running cluster </figcaption>
</figure>

Additionally, you can watch a video demonstration where we navigate to the website hosted on the Kubernetes cluster.
INSERT VIDEO!!!


## GitHub Actions
We implemented a CI/CD using GitHub Actions, such that we can trigger deployment using GitHub Events. The yaml file which sets up the workflow can be found in the folder .github/workflows.

Our pipeline is simple, and does not require data collection nor data processing. Therefore the only Action we define is to setup the Kubernetes cluster with our app deployed. A brief description of the details of the action is listed below:

- the workflow is triggered on a push event to the main branch.
- the job is conditional on the commit message containing /run-deploy-app.
- the workflow runs in Ubuntu, and checks out the repository code
- builds the deployment container with the necessary GC credentials, and runs the script deploy-app.sh, which deploys the latest docker images for the frontend and api-service, and sets up the K8 clusters
