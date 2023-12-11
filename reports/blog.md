MomaLisa
This article was produced as part of the final project for Harvard's AC215 Fall 2023 course.

Table of Contents
1. Introduction
2. API
3. Machine Learning Modelling
4. Front-end
5. Deployment
6. Next steps
7. References

1. Introduction
MOMA Lisa allows users to walk between two artworks in the latent space. What does this mean? A user picks the start and end of their journey and MOMA Lisa generates images that are a fluid transition between the two. For example, one can transition between a giraffe and a battleship and see the output as an animation (REFERENCE TO GIF). 

In this blogpost we explain our inspiration for the project, the machine learning models and the deployment we use. 

2. API 
We use the FastAPI Python implementation of RestAPI to connect our frontend with the backend. The GET request to the api provides the model with two strings which it uses to create `n` continuous images between those two strings. The resulting images are stored in the `saved_predictions` GCP bucket. The frontend then makes an API call through the Google Cloud SDK to the bucket to stream the image. The image is shown on the frontend and the user can download it as well now.  

3. Machine Learning Modelling
The animations are generated with StableDiffusion. The user inputs two strings in our frontend. An image embedding generates latent space representations of these two images. We then draw a high dimensional line between the two points and pick new points along this line. For each of those `n` points we generate an artwork by forwarding the representation through the repitive U-Net element of the StableDiffusion architecture. This results in `n` images. 

To ensure a smooth transition between the final images we have to fix the noise added to the latent representation. Adding equal noise to all `n` during the image generation ensures that the final outputs create the illusion of continuity which is essential for the animation. 

4. Front-end

5. Deployment

6. Next steps

7. References
