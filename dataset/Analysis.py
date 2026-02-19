import pandas as pd

# 1) Cargar datos ficticios
df = pd.read_csv("dataset/data.csv")

# 2) Normalizar tipos
df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
df["device_start_date"] = pd.to_datetime(df["device_start_date"], errors="coerce")
df["device_end_date"] = pd.to_datetime(df["device_end_date"], errors="coerce")

df["sex"] = df["sex"].astype(str).str.upper().str.strip()
df["device_type"] = df["device_type"].astype(str).str.upper().str.strip()

df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")
df["height_cm"] = pd.to_numeric(df["height_cm"], errors="coerce")
df["usage_hours"] = pd.to_numeric(df["usage_hours"], errors="coerce")

# 3) Variables derivadas
today = pd.Timestamp("today").normalize()
df["age"] = ((today - df["birth_date"]).dt.days / 365.25).astype("float")

df["bmi"] = df["weight_kg"] / ((df["height_cm"] / 100) ** 2)
df["usage_duration_days"] = (df["device_end_date"] - df["device_start_date"]).dt.days

# 4) Reglas de validación (Data Quality)
df["rule_missing_birth_date"] = df["birth_date"].isna()
df["rule_invalid_sex"] = ~df["sex"].isin(["F", "M"])
df["rule_invalid_weight"] = df["weight_kg"].isna() | (df["weight_kg"] < 30) | (df["weight_kg"] > 250)
df["rule_invalid_height"] = df["height_cm"].isna() | (df["height_cm"] < 120) | (df["height_cm"] > 220)

df["rule_invalid_dates"] = df["device_start_date"].isna() | df["device_end_date"].isna() | (df["device_end_date"] < df["device_start_date"])
df["rule_invalid_usage"] = df["usage_hours"].isna() | (df["usage_hours"] < 0) | (df["usage_hours"] > 24 * 365)  # límite razonable

# 5) Duplicados potenciales (mismo paciente + dispositivo + inicio)
dup_cols = ["patient_id", "device_type", "device_start_date"]
df["rule_duplicate"] = df.duplicated(subset=dup_cols, keep=False)

# 6) Flag final
rules = [c for c in df.columns if c.startswith("rule_")]
df["data_quality_flag"] = df[rules].any(axis=1)

# 7) Métricas de calidad
metrics = {
    "total_records": int(len(df)),
    "invalid_pct": float(df["data_quality_flag"].mean()),
    "missing_birth_date_pct": float(df["rule_missing_birth_date"].mean()),
    "invalid_dates_pct": float(df["rule_invalid_dates"].mean()),
    "duplicate_pct": float(df["rule_duplicate"].mean()),
}
print("DATA QUALITY METRICS")
for k, v in metrics.items():
    print(f"- {k}: {v:.2%}" if "pct" in k else f"- {k}: {v}")

# 8) Export limpio (para análisis)
df.to_csv("dataset/data_clean.csv", index=False)
print("\nArchivo generado: dataset/data_clean.csv")
