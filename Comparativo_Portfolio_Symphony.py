import pandas as pd

# === 1. Leer los archivos ===
# Symphony exportado como CSV UTF-8
df_symphony = pd.read_csv("bnco/Symphony_30_07_2025.csv", sep=";", encoding="utf-8", dtype=str)

# Portfolio viene como TXT tabulado
df_portfolio = pd.read_csv("bnco/Portfolio_22_08_2025.txt", sep="\t", encoding="utf-8", dtype=str)

# --- 2. Expandir Symphony (una fila por cada URL) ---
df_symphony_expanded = df_symphony.assign(
    url = df_symphony["856$u"].str.split(";")
).explode("url")

# Quitar espacios en blanco
df_symphony_expanded["url"] = df_symphony_expanded["url"].str.strip()
print("df_symphony_expanded")
#print(df_symphony_expanded.head()) 

# --- 3. Unir Symphony vs Port folio ---
merged = df_symphony_expanded.merge(
    df_portfolio,
    how="outer",
    left_on="url",
    right_on="URL",
    indicator=True
)

# --- 4. Ver el resumen ---
print(merged["_merge"].value_counts())

# --- 5.Separar resulados
solo_symphony = merged[merged["_merge"] == "left_only"]["url"].dropna().unique()
solo_portfolio = merged[merged["_merge"] == "right_only"]["URL"].dropna().unique()
em_ambos = merged[merged["_merge"] == "both"]["url"].dropna().unique()


print("🔹 Solo en Symphony:", len(solo_symphony))
print("🔹 Solo en Portfolio:", len(solo_portfolio))
print("🔹 En ambos:", len(em_ambos))

print(merged.head(1).to_string(index=False))

merged.to_excel("Comparativo_Symphony_Portfolio.xlsx", index=False)

"""
# === 5. Armar DataFrame final ===
df_result = pd.DataFrame({
    "URL": list(solo_symphony) + list(solo_portfolio) + list(en_ambos),
    "Estado": (["Solo en Symphony"] * len(solo_symphony)) +
              (["Solo en Portfolio"] * len(solo_portfolio)) +
              (["En ambos"] * len(en_ambos))
})

# === 6. Exportar a Excel ===
df_result.to_excel("comparacion_symphony_portfolio.xlsx", index=False, encoding="utf-8")

print("✅ Comparación lista: comparacion_symphony_portfolio.xlsx")
"""

