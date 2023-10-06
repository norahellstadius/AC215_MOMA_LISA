#!/bin/bash

# variables
# TODO: change these to be parsed in
repository_url="https://github.com/huggingface/diffusers.git"
destination_dir="../diffusers"
#model_name="CompVis/stable-diffusion-v1-4"
#train_dir="path_to_your_dataset"
#output="path_to_save_model"
export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export dataset_name="lambdalabs/pokemon-blip-captions"

# clone repository
if [ ! -d "$destination_dir" ]; then
  git clone "$repository_url" "$destination_dir"
fi

# TODO: move train.py to
mv train_text_to_image.py "${destination_dir}/examples/text_to_image/train_text_to_image.py"

cd "${destination_dir}/examples/text_to_image"

# setup virtual environment
if [ ! -d "momalisa" ]; then
    python3 -m venv momalisa
fi
. ./momalisa/bin/activate

# install packages
pip install -r requirements.txt
pip install git+https://github.com/huggingface/diffusers.git
pip install wandb

# set global variables
export MODEL_NAME=$model_name
export TRAIN_DIR=$train_dir
export OUTPUT_DIR=$output_dir

# initialize accelerate environment
# TODO: change to accelarate config --default
accelerate config

# wandb setup
json_file="../../../../secrets/wandb_api_key.json"
if [ ! -s ~/.netrc ]; then
    API_KEY=$(cat "${json_file}")
    wandb login $API_KEY
else
    wandb login
fi


# run code
#accelerate launch train_text_to_image.py \
#  --pretrained_model_name_or_path=$model_name \
#  --train_data_dir=$train_dir \
#  --use_ema \
#  --resolution=512 --center_crop --random_flip \
#  --train_batch_size=1 \
#  --gradient_accumulation_steps=4 \
#  --gradient_checkpointing \
#  --mixed_precision="fp16" \
#  --max_train_steps=15000 \
#  --learning_rate=1e-05 \
#  --max_grad_norm=1 \
#  --lr_scheduler="constant"
#  --lr_warmup_steps=0 \
#  --output_dir=$output_dir \
#  --push_to_hub
accelerate launch --mixed_precision="fp16"  train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$dataset_name \
  --use_ema \
  --resolution=512 --center_crop --random_flip \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --max_train_steps=15000 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir="sd-pokemon-model" \
  --push_to_hub