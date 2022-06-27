from tensorflow.keras.models import load_model
import os
import sklearn
import numpy as np

# Gather input (model)
model_path = os.path.join(os.environ["INPUT_FOLDER"], "model.h5")
input_data_path = os.path.join(os.environ["INPUT_FOLDER"], "predict_data.npy")

# Load model
model = load_model(model_path)
print("Loaded model:")
model.summary()

# Load data
inputData = np.load(input_data_path)
print(f"Loaded input data with dimension {inputData.shape}")
print(f"Evaluation samples {inputData.shape[0]}")

# Predict
out = model.predict(inputData, verbose=2)

# Save predictions
print(f"Saving predictions to output with dimension {out.shape}")
out_path = os.environ["OUTPUT_FOLDER"]
np.save(os.path.join(out_path, "predictions.npy"), out)

