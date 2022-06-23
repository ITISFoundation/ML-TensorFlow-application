import tensorflow as tf
from tensorflow.keras.models import load_model
import os, json
import numpy as np

# Gather inputs
train_data_path = os.path.join(os.environ["INPUT_FOLDER"], "train_data.npy")
train_label_path = os.path.join(os.environ["INPUT_FOLDER"], "train_label.npy")
validation_data_path = os.path.join(os.environ["INPUT_FOLDER"], "validation_data.npy")
validation_label_path = os.path.join(os.environ["INPUT_FOLDER"], "validation_label.npy")
model_path = os.path.join(os.environ["INPUT_FOLDER"], "model.h5")

input_dict = json.load(open(os.path.join(os.environ["INPUT_FOLDER"], "inputs.json"),"r"))

epochs = input_dict["input_6"]
batch_size = input_dict["input_7"]

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
print(f"\nPrinting model architecture")
model.summary()

# Fit model
print(f"Firing model with epochs={epochs} and batch_size={batch_size}")
model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_data=val, verbose=2)

# Save model to output folder
outputFile = os.path.join(os.environ["OUTPUT_FOLDER"], "model.h5")
model.save(outputFile)

print(f"Stored model with size {os.path.getsize(outputFile) * 1e-6:.2f} MB \n")






