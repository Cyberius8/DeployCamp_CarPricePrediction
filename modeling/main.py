import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn_quantile import RandomForestQuantileRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocessing import load_and_preprocess

# Setup MLflow ke Dagshub
mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")
mlflow.set_experiment("Car Price Prediction")

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    return mae, rmse, r2

def main():
    # Load dan preprocessing data
    df, _ = load_and_preprocess("https://raw.githubusercontent.com/Cyberius8/DeployCamp_CarPricePrediction/refs/heads/main/data/CarPrice_Assignment.csv")

    selected_features = ['brand', 'wheelbase', 'carlength', 'carwidth', 'curbweight', 'enginesize', 'fuelsystem', 'boreratio', 'horsepower']
    X = df[selected_features]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Definisi model + hyperparameters
    models = {
        "LinearRegression": {
            "model": LinearRegression(),
            "params": {}
        },
        "XGBRegressor": {
            "model": XGBRegressor(learning_rate=0.05, random_state=42),
            "params": {"learning_rate": 0.05}
        },
        "RandomForest": {
            "model": RandomForestRegressor(n_estimators=100, random_state=42),
            "params": {"n_estimators": 100}
        },
        "QuantileRF": {
            "model": RandomForestQuantileRegressor(
                n_estimators=100, q=[0.025, 0.5, 0.975], random_state=42
            ),
            "params": {"n_estimators": 100, "quantiles": [0.025, 0.5, 0.975]}
        }
    }

    # Training + Logging
    for name, entry in models.items():
        model = entry["model"]
        params = entry["params"]

        with mlflow.start_run(run_name=name) as run:
            model.fit(X_train, y_train)

            # evaluasi model
            if name == "QuantileRF":
                q_lower, q_median, q_upper = model.predict(X_test)
                mae = mean_absolute_error(y_test, q_median)
                rmse = np.sqrt(mean_squared_error(y_test, q_median))
                r2 = r2_score(y_test, q_median)
            else:
                mae, rmse, r2 = evaluate_model(model, X_test, y_test)

            print(f"[{name}] MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}")

            # log params, metrics, model artifact
            mlflow.log_params(params)
            mlflow.log_metrics({"MAE": mae, "RMSE": rmse, "R2": r2})
            mlflow.sklearn.log_model(model, name)

            # Register model ke Model Registry DagsHub
            model_uri = f"runs:/{run.info.run_id}/{name}"
            mlflow.register_model(model_uri, name)


    print("🚀 Training selesai dan sudah di-log ke MLflow Dagshub!")

if __name__ == "__main__":
    main()