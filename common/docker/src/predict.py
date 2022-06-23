from tensorflow.keras.models import load_model
import os
import numpy as np

# Gather input (model)
model_path = os.path.join(os.environ["INPUT_FOLDER", "model.h5"])
input_data_path = os.path.join(os.environ["INPUT_FOLDER", "predict_data.npz"])

# Load model
model = load_model(model_path)
print("Loaded model:")
model.summary()

# Load data
inputData = np.load(input_data_path)
print(f"Loaded input data with dimension {inputData.shape}")

# Predict
out = model.predict(inputData)

# Save predictions
out_path = os.environ["OUTPUT_1"]
np.savetxt(os.path.join(out_path, "predictions.csv"), out, delimiter=",")
