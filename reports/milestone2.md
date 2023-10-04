# What's Cookin'
### Nora Hallqvist, Anna Midgley, Sebastian Weisshaar


## Milestone 2
The two steps of the data pipeline, are scraping data from BBC Good Foods and processing this data. 
For this milestone, we created two containers, atomic for each step, ensuring that each step can be run independently.
The containers are built using the Dockerfiles, with their images uploaded to [DockerHub-scrape](https://hub.docker.com/repository/docker/amidgley/scrape/general)
and [DockerHub-preprocess](https://hub.docker.com/repository/docker/amidgley/preprocess/general).

The main steps of the DockerFile: 
1. Pull a base image from DockerHub (using Slim Debian Buster distribution)
2. Set environment variables
3. System updates & package installation
4. Set the working directory
5. Add source code
6. Set the entrypoint of the container as a bash shell.
    
In the first step - scrape - we will scrape BBC Good Foods for recipes and images, saving the data to a GCP bucket. In
the second step - preprocess - we will process the data, pulling from the scrape bucket, and save the processed data to 
another GCP bucket. We have set up these two buckets as well as a service account, allowing the automation of this process. 
The project name is `cook_this`, and the two buckets are respectively `cook_this_scrape` and `cook_this_preprocess`.

The data is not live, and therefore our project will not require data version control (dvc). We have used `PipFile` and `PipFile.lock` to 
manage our package dependencies tailored for each container. 

To run the containers, we have used the following commands:
```
docker-compose run scrape 
docker-compose run preprocess
```