#!/bin/bash

# variables
RESPOSITORY_URL="https://github.com/huggingface/diffusers.git"
DESR_DIR="../diffusers"

# clone repository
if [ ! -d "$DESR_DIR" ]; then
  git clone "$RESPOSITORY_URL" "$DESR_DIR"
fi

# mve train script

cp "train/train_text_to_image.py" "${DESR_DIR}/examples/text_to_image/train_text_to_image.py"

python "train/fetch_train_data.py"
>>>>>>> 78898c7fe71645536578068094815184b13e0fe3
