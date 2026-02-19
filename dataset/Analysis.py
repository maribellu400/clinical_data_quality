import pandas as pd
from datetime import datetime

df = pd.read_csv("dataset/patient_usage.csv")

# fechas
df["birth_date"] = pd.to_datetime(df["birth_date"])
df["device_start_date"] = pd.to_datetime(df["device_start_date"])
df["device_end_date"] = pd.to_datetime(df["device_end_date"])

# edad
today = pd.Timestamp("today")
df["age"] = (today - df["birth_date"]).dt.days // 365

# BMI
df["bmi"] = df["weight_kg"] / ((df["height_cm"]/100)**2)

# duración
df["usage_duration_days"] = (df["device_end_date"] - df["device_start_date"]).dt.days

# validaciones
df["invalid_usage"] = df["usage_hours"] < 0
df["invalid_dates"] = df["usage_duration_days"] < 0
df["missing_weight"] = df["weight_kg"].isna()

df["data_quality_flag"] = (
    df["invalid_usage"] |
    df["invalid_dates"] |
    df["missing_weight"]
)

print(df[["patient_id","data_quality_flag"]])

df.to_csv("dataset/patient_usage_clean.csv", index=False)

