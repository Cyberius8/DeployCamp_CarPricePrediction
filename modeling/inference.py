import pandas as pd
import mlflow.sklearn

# Tracking URI ke Dagshub
mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")

# Nama model yang ingin digunakan
model_name = "RandomForest"
model_uri = f"models:/{model_name}/latest"

# Load model
model = mlflow.sklearn.load_model(model_uri)

# Contoh data baru
new_data = pd.DataFrame({
    'brand': [2],    
    'wheelbase': [98.0],
    'carlength': [180.0],
    'carwidth': [66.5],
    'curbweight': [2500],
    'enginesize': [130],
    'fuelsystem': [0],
    'boreratio': [3.15],
    'horsepower': [111]
})

# Prediksi
if model_name == "QuantileRF":
    q_lower, q_median, q_upper = model.predict(new_data)
    print("🎯 Prediksi Harga Mobil (Quantile RF):")
    print(f"Lower Bound (2.5%):  Rp {q_lower[0]:,.2f}")
    print(f"Median (50%):        Rp {q_median[0]:,.2f}")
    print(f"Upper Bound (97.5%): Rp {q_upper[0]:,.2f}")
else:
    prediction = model.predict(new_data)[0]
    print(f"🎯 Prediksi Harga Mobil (Point Estimate): Rp {prediction:,.2f}")