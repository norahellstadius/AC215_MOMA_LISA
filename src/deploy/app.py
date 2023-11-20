import logging
import torch
from flask import Flask, jsonify, request
#from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, UNet2DConditionModel, LMSDiscreteScheduler
from torchvision import transforms as tfms
from PIL import Image
import cv2
import base64


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

NUM_STEPS = 4

# Load model and tokenizer
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14", torch_dtype=torch.float16)
text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-large-patch14", torch_dtype=torch.float16).to("cuda")
vae = AutoencoderKL.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="vae", torch_dtype=torch.float16).to("cuda")
unet = UNet2DConditionModel.from_pretrained("CompVis/stable-diffusion-v1-4", subfolder="unet", torch_dtype=torch.float16).to("cuda")
scheduler = LMSDiscreteScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", num_train_timesteps=1000)
scheduler.set_timesteps(50)

# Check if CUDA is available and log the info
using_cuda = torch.cuda.is_available()
logger.info(f"Using CUDA: {using_cuda}")

def numpy_array_to_base64(array):
    _, buffer = cv2.imencode('.png', array)
    encoded_string = base64.b64encode(buffer)
    return encoded_string.decode('utf-8')

def load_image(p):
    '''
    Function to load images from a defined path
    '''
    return Image.open(p).convert('RGB').resize((512,512))

def pil_to_latents(image):
    '''
    Function to convert image to latents
    '''
    init_image = tfms.ToTensor()(image).unsqueeze(0) * 2.0 - 1.0
    init_image = init_image.to(device="cuda", dtype=torch.float16)
    init_latent_dist = vae.encode(init_image).latent_dist.sample() * 0.18215
    return init_latent_dist

def latents_to_base64(latents):
    '''
    Function to convert latents to images
    '''
    latents = (1 / 0.18215) * latents
    with torch.no_grad():
        image = vae.decode(latents).sample
    image = (image / 2 + 0.5).clamp(0, 1)
    image = image.detach().cpu().permute(0, 2, 3, 1).numpy()
    images = (image * 255).round().astype("uint8")
    base64_imgs = [numpy_array_to_base64(image)for image in images]
    return base64_imgs

def text_enc(prompts, maxlen=None):
    '''
    A function to take a texual promt and convert it into embeddings
    '''
    if maxlen is None: maxlen = tokenizer.model_max_length
    inp = tokenizer(prompts, padding="max_length", max_length=maxlen, truncation=True, return_tensors="pt")
    return text_encoder(inp.input_ids.to("cuda"))[0].half()


def produce_walk(prompt1: str, prompt2: str, steps: int):
  # Defining batch size
    bs = steps
    dim=512
    g=7.5

    space = torch.linspace(0, 1, steps, dtype=torch.float16).view(-1, 1, 1).to('cuda')
    # Converting textual prompts to embedding
    text = text_enc([prompt1, prompt2])
    t1 = text[0]
    t2 = text[1]
    text = space * t1 + (1 - space) * t2

    # Adding an unconditional prompt , helps in the generation process
    uncond =  text_enc([""] * bs, text.shape[1])
    emb = torch.cat([uncond, text])

    # Setting the seed
    torch.manual_seed(99)

    # Initiating random noise
    latents = torch.randn((bs, unet.in_channels, dim//8, dim//8))
    scheduler.set_timesteps(70)
    latents = latents.to("cuda").half() * scheduler.init_noise_sigma

    # Iterating through defined steps
    for i,ts in enumerate(scheduler.timesteps):
        # We need to scale the i/p latents to match the variance
        inp = scheduler.scale_model_input(torch.cat([latents] * 2), ts)

        # Predicting noise residual using U-Net
        with torch.no_grad(): u,t = unet(inp, ts, encoder_hidden_states=emb).sample.chunk(2)

        # Performing Guidance
        pred = u + g*(t-u)

        # Conditioning  the latents
        latents = scheduler.step(pred, ts, latents).prev_sample

    return latents

#-------------- Tale code -----------------
@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["POST"])
def predict(endpoint_id, deployed_model_id):
    try:
        # Validate and extract input_text from request JSON
        instances = request.json.get("instances")
        if not instances or not all(isinstance(instance, dict) for instance in instances):
            logger.error("Invalid input_text")
            return jsonify(error="Invalid input_text"), 400

        # Placeholder for generated texts
        generated_set_imgs = []

        # Generate text for each input instance
        for instance in instances:
            input_text = instance.get("sample_key")
            if not input_text or not isinstance(input_text, list):
                logger.error("Invalid input_text in one or more instances")
                return jsonify(error="Invalid input_text in one or more instances"), 400

            latent_output = produce_walk(input_text[0], input_text[1], NUM_STEPS)
            img_set= latents_to_base64(latent_output)
            # output = model.generate(input_ids, max_length=100, num_beams=5, temperature=1.5)
            generated_set_imgs.append(img_set)

        # Return the generated texts
        return jsonify(predictions=generated_set_imgs), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500


@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["GET"])
def get_model_info(endpoint_id, deployed_model_id):
    try:
        # [Optional] You may use endpoint_id and deployed_model_id to
        # manage and fetch specific model info
        # Example: Fetch and return some information about the model
        model_info = {
            "model_name": "stable_diffusion",
            "endpoint_id": endpoint_id,
            "deployed_model_id": deployed_model_id,
        }
        return jsonify(model_info), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)