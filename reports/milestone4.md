
**Project Description:**
Our project takes a user's prompt for two points, and generates a continuous series MoMa artworks transitioning between them.
We achieve this by transversing through the latent space, creating intermediate points between the two given points, from which we can decode 
and generate images from. The images are then used to produce a gif, which is displayed to the user.

**Project Journey:**
This is not the first topic we have investigated in this project. Previously, we were hoping
to use image and generated caption pairs, to fine-tune a stable diffusion model on MoMA artworks. We set
up severless training, that utilized images & captions stored in a GCP bucket with WandB used to track
model training. However, we realized that we were unable to teach the model anything. For this reason,
we decided to pivot to a different idea. We experimented with instead trying to learn specific lesser known
artists styles. Unfortunately we realized that for any artist that had satisfactory set of artworks available,
the model already knew the style, and again found ourselves unable to teach the model anything. Thus, we have switched
to our current topic. It should be noted that the following folders of work in `src` are from previous project
ideas and not applicable to our current idea: `train`, `preprocess`, `scrape`, `data`. 

