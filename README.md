# What's Cookin'
### Nora Hallqvist, Anna Midgley, Sebastian Weisshaar


## Milestone 2
The two steps of the data pipeline, are scraping data from BBC Good Foods and processing this data. 
For this milestone, we created two containers, atomic for each step, ensuring that each step can be run independently.
The containers are built using the Dockerfiles, with their images uploaded to [DockerHub](https://hub.docker.com/repository/docker/amidgley/scrape/general).
We have used the following commands in creating the containers:
```
```
    
In the first step - scrape - we will scrape BBC Good Foods for recipes and images, saving the data to a GCP bucket. In
the second step - preprocess - we will process the data, pulling from the scrape bucket, and save the processed data to 
another GCP bucket. We have set up these two buckets as well as a service account, allowing the automation of this process. 

The data is not live, and therefore our project will not require data version control (dvc). We have used `PipFile` and `PipFile.lock` to 
manage our package dependencies tailored for each container. 