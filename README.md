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
        

## AC215 - Milestone 5 - MOMA Lisa

This Milestone encompassed:
1. Application Design Document
2. APIs & Frontend Implementation

### Application Design Document
**Solution Architecture:**
The solution architecture for our application is spit between process, execution and state. The solution architecture 
subsections are described in the diagram below, and the entire flow diagram linking the subsections depicted in the diagram after. 

<figure>
    <img src="./imgs/solution_architecture.png" height="500" />
    <figcaption>MoMA Lisa Solution Architecture SubSections </figcaption>
</figure>

<figure>
    <img src="./imgs/solution_architecture_pipeline.png" height="500" />
    <figcaption>MoMA Lisa Solution Architecture Flow Diagram</figcaption>
</figure>

**Technical Architecture:**
The technical architecture provides a high level view from development to deployment, illustrating the interactions
between components and containers. It provides the blueprint of the system, helping to understand how the system will work. 

For source control, we will use GitHub to keep track of our code & the changes to it. We will use Vertex AI & GCP for model deployment, 
and GCR to host the needed container images. GCS buckets will be used to store the outputted gifs. GCE persistent volume
will be used to store any files that need to be persisted when container images are updated. We will use a virtual machine instance
on GCE to host a single instance with all the needed containers running on it. 

The technical architecture, and the interactions between the components and containers are depicted in the diagram below.

<figure>
    <img src="./imgs/technical_architecture.png" height="500" />
    <figcaption>MoMA Lisa Technical Architecture </figcaption>
</figure>

### APIs & Frontend Implementation
**API Service/Backend:**
The backend API service connects to our deployed model which is hosted on Vertex AI. This allows us to make predictions, 
generating images along the latent space walk. When we call the model, the predictions are also written to a GCP bucket.

**Deploying the Model on Vertex AI**
Before launching the website, the model stored on Vertex AI must be deployed. These steps must be completed:  
1. Navigate to the Vertex AI on Google Cloud.
2. In the Model Registry, select the region as US-east1.
3. Locate and click on the model named "diffusion-vertexai-4."
4. Under the "Deploy and Test" tab, click on "Deploy to Endpoint."
5. In the deployment configuration, choose "NVIDIA_TESLA_T4" as the accelerator type.
6. After the model is successfully deployed, copy the provided ID number.
7. Open the Python file named `model.py` found in `src/api-service/api`.
8. Locate the following line of code in `model.py`:

    ```python
    endpoint = aiplatform.Endpoint(
        "projects/580339194016/locations/us-east1/endpoints/{ID}"
    )
    ```

9. Replace `{ID}` with the copied ID number from the deployed model.
Now, the model is linked to the correct endpoint, and you can proceed with launching the website.

**Frontend:**
The frontend we have created allows a user to input two objects, from which a gif will be generated that captures the latent space walk. The generated gif is placed on the left side of the webise and can be downloaded from the website. 

Our website additionally has a GIF gallery, where users can view previously generated gifs and gain inspiration. Lastly it has a small section discussing the project, link to our source code, and the team members. Please refer to the image below to see how the user interacts with the website to generate and download a gif. In addition a video is provided below for a tour of the webiste. 

<figure>
    <img src="./imgs/first_page.png" height="500" />
    <figcaption>Part of website where user inputs prompts and can generate a GIF</figcaption>
</figure>


### Video 
Check out a demo of our project [here](https://youtu.be/PUSkKIgtY2E)

### Ansible
Ansible is a tool that allows us to automate the deployment of our application. The following commands are used to deploy our application:
1. Build the deployment container: `sh docker-shell.sh`
2. Build & push docker containers to GCR (if you haven't already): `ansible-playbook deploy-docker-images.yml -i inventory.yml`
3. Create a VM instance in GCP: `ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present`
4. Provision the VM instance: `ansible-playbook deploy-provision-instance.yml -i inventory.yml`
- note: check that the VM instance on GCP external IP matches the one in inventory.yml
5. Set up the containers: `ansible-playbook deploy-setup-containers.yml -i inventory.yml`
6. Check that containers are running by SSH into instance & running `sudo docker container ls` or `sudo docker container logs api-service -f`
7. Deploy the webserver: `ansible-playbook deploy-setup-webserver.yml -i inventory.yml`
8. Visit the website by using the external IP address of the VM: `http://<external_ip>`

To delete the VM instance, run the following command: `ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent`

These commands take care of creating the different docker images, uploading them to GCR, creating a VM instance, 
establishing a docker network, running the docker containers and creating a webserver managed by NGINX.

### Future Work
We note that currently we are only generate 4 points in the latent space walk between the two user inputted points. The result of this
is that the latent space walk is coarse, and does not smoothly transition from one object to the next. The reason we have set the value is so low, is that 
for any higher number of points there is a timeout when calling our model. The reason for this is that a diffusion model is a large model, 
that takes considerable time to predict. We would like to improve this in order to generate smoother gifs. We would like to explore 
deploying multiple models in parallel, and then splitting the predictions across these models so 
that neither time out, also reducing latency. We plan to explore this in our final milestone of the project, when we focus
on scalability.