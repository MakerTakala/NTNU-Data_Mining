import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    data = pd.read_csv("../vgsales.csv")
    label = [
        "Rank",
        "Name",
        "Platform",
        "Year",
        "Genre",
        "Publisher",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales",
    ]

    for col in [
        "Year",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales",
    ]:
        imputer = SimpleImputer(
            missing_values=np.nan, strategy="constant", fill_value=0
        )
        data[col] = imputer.fit_transform(data[col].values.reshape(-1, 1))

    for col in ["Platform", "Genre", "Publisher"]:
        label_encoder = LabelEncoder()
        data[col] = label_encoder.fit_transform(data[col])

    for col in [
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales",
    ]:
        min_max_scaler = MinMaxScaler()
        data[col] = min_max_scaler.fit_transform(data[col].values.reshape(-1, 1))

    trainset, testset = train_test_split(data, test_size=0.2, random_state=0)
    print(trainset, testset)
