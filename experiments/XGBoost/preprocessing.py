import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess(csv_path='https://raw.githubusercontent.com/Cyberius8/DeployCamp_CarPricePrediction/refs/heads/main/data/CarPrice_Assignment.csv'):
    df = pd.read_csv(csv_path)
    
    # Drop kolom tidak penting
    df = df.drop(columns=['car_ID', 'symboling'])

    # Normalisasi nama mobil dan ekstraksi brand
    df['CarName'] = df['CarName'].str.lower()
    df['CarName'] = df['CarName'].replace({
        'maxda': 'mazda', 'porcshce': 'porsche',
        'toyouta': 'toyota', 'vw': 'volkswagen'
    })
    df['brand'] = df['CarName'].apply(lambda x: x.split(' ')[0])
    df.drop(columns=['CarName'], inplace=True)

    # Konversi harga ke IDR
    df['price'] = df['price'] * 16314

    # Encoding kolom kategorikal
    cat_cols = df.select_dtypes(include='object').columns
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders