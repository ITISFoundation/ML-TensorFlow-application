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
print(f"Loaded input data with dimension {inputData.shape}")

# Predict
out = model.evaluate(inputData, verbose=2)

#print(f"Evaluating results...\n")
#for name, val in zip(model.metrics_names, out):
#    print(f"{name:.6f}: {val:.6f}")

