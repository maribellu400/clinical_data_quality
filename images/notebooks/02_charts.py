import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Config paths ---
RAW_PATH = "dataset/data.csv"
CLEAN_PATH = "dataset/data_clean.csv"
OUT_DIR = "images"

os.makedirs(OUT_DIR, exist_ok=True)

# --- Load data (prefer clean) ---
path = CLEAN_PATH if os.path.exists(CLEAN_PATH) else RAW_PATH
df = pd.read_csv(path)

# --- If rules columns exist, we can plot % invalid by rule ---
rule_cols = [c for c in df.columns if c.startswith("rule_")]

# ---------------------------
# 1) % inválidos por regla
# ---------------------------
if rule_cols:
    pct_by_rule = (df[rule_cols].mean() * 100).sort_values(ascending=False)

    plt.figure()
    plt.bar(pct_by_rule.index, pct_by_rule.values)
    plt.title("% de registros marcados por regla de validación")
    plt.ylabel("Porcentaje (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "invalid_pct_by_rule.png"), dpi=160)
    plt.close()
else:
    print("No se encontraron columnas rule_. Saltando gráfico 1.")

# ---------------------------
# 2) Uso promedio por dispositivo
# ---------------------------
# Espera: device_type y usage_hours
if "device_type" in df.columns and "usage_hours" in df.columns:
    # Convertir a numérico por si viene como texto
    df["usage_hours"] = pd.to_numeric(df["usage_hours"], errors="coerce")

    avg_usage = df.groupby("device_type")["usage_hours"].mean().sort_values(ascending=False)

    plt.figure()
    plt.bar(avg_usage.index.astype(str), avg_usage.values)
    plt.title("Uso promedio (horas) por tipo de dispositivo")
    plt.ylabel("Horas promedio")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "avg_usage_by_device.png"), dpi=160)
    plt.close()
else:
    print("Faltan columnas device_type o usage_hours. Saltando gráfico 2.")

# ---------------------------
# 3) Distribución de edades
# ---------------------------
# Si ya existe age perfecto; si no, intentamos calcular desde birth_date
if "age" not in df.columns and "birth_date" in df.columns:
    bd = pd.to_datetime(df["birth_date"], errors="coerce")
    today = pd.Timestamp("today").normalize()
    df["age"] = ((today - bd).dt.days / 365.25)

if "age" in df.columns:
    ages = pd.to_numeric(df["age"], errors="coerce").dropna()

    plt.figure()
    plt.hist(ages, bins=10)
    plt.title("Distribución de edades")
    plt.xlabel("Edad")
    plt.ylabel("Cantidad de registros")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "age_distribution.png"), dpi=160)
    plt.close()
else:
    print("No se encontró age ni birth_date. Saltando gráfico 3.")

print("Listo. Imágenes generadas en /images")

