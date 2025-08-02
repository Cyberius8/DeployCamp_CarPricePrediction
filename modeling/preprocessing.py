import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess(path: str):
    # Load dataset
    df = pd.read_csv(path)

    # Drop kolom tidak berguna
    df = df.drop(columns=['car_ID', 'symboling'])

    # Normalisasi CarName
    df['CarName'] = df['CarName'].str.lower()

    # Ambil brand dari CarName
    df['brand'] = df['CarName'].apply(lambda x: x.split(' ')[0])
    df = df.drop(columns=['CarName'])

    # Normalisasi brand
    df['brand'] = df['brand'].replace({
        'maxda': 'mazda',
        'porcshce': 'porsche',
        'toyouta': 'toyota',
        'vw': 'volkswagen',
        'vokswagen': 'volkswagen',
        'alfa-romero': 'alfa-romeo'
    })

    # Konversi price ke IDR
    df['price'] = df['price'] * 16000

    # Encoding kolom kategori
    cat_cols = df.select_dtypes(include='object').columns
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders