FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

# Set the working directory
WORKDIR /workspace

# Copy only the dependencies file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py ./

# Start the application
CMD ["python", "app.py"]