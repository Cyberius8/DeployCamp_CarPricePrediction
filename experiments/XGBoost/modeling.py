import numpy as np
import mlflow
import mlflow.xgboost
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from preprocessing import load_and_preprocess

# Set MLflow Tracking ke DagsHub
mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")
mlflow.set_experiment("XGBoost Car Price Prediction")

def train_and_log_model(df):
    selected_features = [
        'enginesize', 'highwaympg', 'curbweight', 'fuelsystem',
        'brand', 'carlength', 'enginetype', 'stroke',
        'horsepower', 'carwidth'
    ]

    X = df[selected_features]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(learning_rate=0.05, random_state=42)

    with mlflow.start_run():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Logging params
        mlflow.log_params({
            "learning_rate": 0.05,
            "model_type": "XGBRegressor",
            "selected_features": ', '.join(selected_features)
        })

        # Logging metrics
        mlflow.log_metrics({
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        })

        # Cross-validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
        mlflow.log_metric("CV_R2_mean", np.mean(cv_scores))

        # Log model
        mlflow.xgboost.log_model(model, artifact_path="xgb_model")

        print(f"MAE: {mae:.2f}, R2: {r2:.4f}, CV_R2_mean: {np.mean(cv_scores):.4f}")

if __name__ == "__main__":
    df, _ = load_and_preprocess()
    train_and_log_model(df)