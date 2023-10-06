#!/bin/bash

DESR_DIR="../diffusers"
cd "${DESR_DIR}/examples/text_to_image"

# install packages
pip install git+https://github.com/huggingface/diffusers.git

# set global variables
export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export TRAIN_DIR="./train/train_data"
export OUTPUT_DIR="moma-sd-finetuned"

# initialize accelerate environment
accelerate config default

# wandb setup
cd "/../.."
api_key_file="$WANDB_API_KEY_PATH"
key=$(cat "$api_key_file")
wandb login $key

# run training
accelerate launch "diffusers/examples/text_to_image/train_text_to_image.py" \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --use_ema \
  --resolution=512 --center_crop --random_flip \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --mixed_precision="fp16" \
  --max_train_steps=50000 \
  --learning_rate=1e-06 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir=${OUTPUT_DIR} \
  --validation_prompts "A MOMA artwork of: changing seasons" "A MOMA artwork of: a coffee" "A MOMA artwork of: an industrial setting" "A MOMA artwork of: critique of the USA" "A MOMA artwork of: Picasso and Monet combined"  \
  --num_train_epochs=100 \
  --report_to="wandb"