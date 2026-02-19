import pandas as pd

df = pd.read_csv("dataset/data.csv")

# 1) Tipos
df["control_date"] = pd.to_datetime(df["control_date"], errors="coerce")
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["device_type"] = df["device_type"].astype(str).str.upper().str.strip()

# 2) Nulos
df["result_value"] = pd.to_numeric(df["result_value"], errors="coerce")

# 3) Reglas de validación
df["is_missing_result"] = df["result_value"].isna()
df["is_outlier"] = df["result_value"].gt(50) | df["result_value"].lt(0)

# 4) Duplicados potenciales
dup_cols = ["campaign", "device_type", "site", "control_date", "result_value"]
df["is_duplicate"] = df.duplicated(subset=dup_cols, keep=False)

# 5) Score / etiqueta final
df["final_status"] = "OK"
df.loc[df["is_missing_result"] | df["is_outlier"], "final_status"] = "INVALIDO"
df.loc[df["is_duplicate"] & (df["final_status"] == "OK"), "final_status"] = "REVISAR"

# 6) Métricas
metrics = {
    "total_records": len(df),
    "missing_result_pct": df["is_missing_result"].mean(),
    "outlier_pct": df["is_outlier"].mean(),
    "duplicate_pct": df["is_duplicate"].mean(),
    "invalid_pct": (df["final_status"] == "INVALIDO").mean(),
}
print(metrics)

# 7) Export dataset limpio
df.to_csv("dataset/data_clean.csv", index=False)
