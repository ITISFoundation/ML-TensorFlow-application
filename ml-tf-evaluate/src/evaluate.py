from tensorflow.keras.models import load_model
import os, json
import numpy as np

# Gather input (model)
model_path = os.path.join(os.environ["INPUT_FOLDER"], "model.h5")
input_data_path = os.path.join(os.environ["INPUT_FOLDER"], "predict_data.npy")
input_label_path = os.path.join(os.environ["INPUT_FOLDER"], "predict_label.npy")

# Load model
model = load_model(model_path)
print("Loaded model:")
model.summary()

# Load data
inputData = np.load(input_data_path)
inputlabel = np.load(input_label_path)
groundTruth = np.load(input_label_path)

print(f"Loaded input data with dimension {inputData.shape}")
print(f"Prediction samples {inputData.shape[0]}")

# Predict
out = model.evaluate(inputData, inputlabel, verbose=2)

print(f"Saving evaluation results to file...\n")

outputFile = os.path.join(os.environ["OUTPUT_FOLDER"], "evaluation_output.txt")

with open(outputFile, 'w') as f:
    for name, val in zip(model.metrics_names, out):
        f.write("{}: {} \n".format(name, val))

