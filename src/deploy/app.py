import logging

# import torch
from flask import Flask, jsonify, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Load model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Check if CUDA is available and log the info
# using_cuda = torch.cuda.is_available()
# logger.info(f"Using CUDA: {using_cuda}")


@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["POST"])
def predict(endpoint_id, deployed_model_id):
    try:
        # Validate and extract input_text from request JSON
        instances = request.json.get("instances")
        if not instances or not all(isinstance(instance, dict) for instance in instances):
            logger.error("Invalid input_text")
            return jsonify(error="Invalid input_text"), 400

        # Placeholder for generated texts
        generated_texts = []

        # Generate text for each input instance
        for instance in instances:
            input_text = instance.get("sample_key")
            if not input_text or not isinstance(input_text, str):
                logger.error("Invalid input_text in one or more instances")
                return jsonify(error="Invalid input_text in one or more instances"), 400

            input_ids = tokenizer.encode(input_text, return_tensors="pt")
            output = model.generate(input_ids, max_length=100, num_beams=5, temperature=1.5)
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            generated_texts.append(generated_text)

        # Return the generated texts
        return jsonify(predictions=generated_texts), 200

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
            "model_name": "GPT-2",
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