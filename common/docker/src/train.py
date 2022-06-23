import tensorflow as tf
from tensorflow.keras.models import load_model
import os, json
import numpy as np

from model import get_model

# Gather inputs
train_data_path = os.path.join(os.environ["INPUT_1"], "train_data.npz")
train_label_path = os.path.join(os.environ["INPUT_2"], "train_label.npz")
validation_data_path = os.path.join(os.environ["INPUT_3"], "validation_data.npz")
validation_label_path = os.path.join(os.environ["INPUT_4"], "validation_label.npz")
model_path = os.path.join(os.environ["INPUT_5"], "model.h5")

epochs = json.loads(os.environ["INPUT_2"])
batch_size = json.loads(os.environ["INPUT_3"])

# Load training data
trainX = np.load(train_data_path)
trainY = np.load(train_label_path)

# Load test data, if available
if os.path.exists(validation_data_path):
    val = (np.load(validation_data_path), np.load(validation_label_path))
else:
    val = None

# Load model
model = load_model(model_path)

# Fit model
model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_data=val)

# Save model to output folder
outputFile = os.path.join(os.environ["OUTPUT_FOLDER"], "model.h5")
model.save(outputFile)

print(f"Stored model with size {os.path.getsize(outputFile) * 1e-6:.2f} MB")






