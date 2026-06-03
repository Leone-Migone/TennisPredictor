import pandas as pd
from data_loader import load_data
from preprocessing import create_model_data
matches = load_data()
matches.info()
model_data = create_model_data(matches)
model_data.info()
print(model_data.head())
print(model_data.shape)
print(model_data["target"].value_counts())
print(model_data.isna().sum())