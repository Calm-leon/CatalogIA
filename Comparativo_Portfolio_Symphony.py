import pandas as pd
import os

try:
    # === 1. Leer los archivos ===
    print("📂 Cargando archivos de catálogo...")

    # Symphony exportado como CSV UTF-8
    symphony_path = os.path.join("bnco", "Symphony_30_07_2025.csv")
    if os.path.exists(symphony_path):
        df_symphony = pd.read_csv(symphony_path, sep=";", encoding="utf-8", dtype=str)
        print(f"✅ Symphony cargado: {len(df_symphony)} registros")
        has_symphony = True
    else:
        print("⚠️ Archivo Symphony no encontrado, continuando solo con Portfolio")
        df_symphony = pd.DataFrame(columns=["856$u"])  # DataFrame vacío con columna necesaria
        has_symphony = False

    # Portfolio viene como TXT tabulado
    portfolio_path = os.path.join("bnco", "Portfolio_22_08_2025.txt")
    if not os.path.exists(portfolio_path):
        raise FileNotFoundError(f"Archivo Portfolio no encontrado: {portfolio_path}")

    df_portfolio = pd.read_csv(portfolio_path, sep="\t", encoding="utf-8", dtype=str)
    print(f"✅ Portfolio cargado: {len(df_portfolio)} registros")

except FileNotFoundError as e:
    print(f"❌ Error: {str(e)}")
    exit(1)
except pd.errors.EmptyDataError:
    print("❌ Error: Uno de los archivos CSV está vacío")
    exit(1)
except Exception as e:
    print(f"❌ Error al cargar archivos: {str(e)}")
    exit(1)

if has_symphony:
    try:
        # --- 2. Expandir Symphony (una fila por cada URL) ---
        print("🔄 Procesando datos de Symphony...")
        df_symphony_expanded = df_symphony.assign(
            url = df_symphony["856$u"].str.split(";")
        ).explode("url")

        # Quitar espacios en blanco
        df_symphony_expanded["url"] = df_symphony_expanded["url"].str.strip()
        print(f"✅ Symphony expandido: {len(df_symphony_expanded)} filas")

    except KeyError:
        print("❌ Error: Columna '856$u' no encontrada en archivo Symphony")
        exit(1)
    except Exception as e:
        print(f"❌ Error al procesar Symphony: {str(e)}")
        exit(1)
else:
    # Si no hay Symphony, crear DataFrame vacío
    df_symphony_expanded = pd.DataFrame(columns=["url"])

try:
    # --- 3. Unir Symphony vs Portfolio ---
    print("🔗 Comparando catálogos...")
    merged = df_symphony_expanded.merge(
        df_portfolio,
        how="outer",
        left_on="url",
        right_on="URL",
        indicator=True
    )
    print("✅ Merge completado")

except Exception as e:
    print(f"❌ Error durante comparación: {str(e)}")
    exit(1)

try:
    # --- 4. Ver el resumen ---
    print("\n📊 Resumen de comparación:")
    print(merged["_merge"].value_counts())

    # --- 5. Separar resultados
    solo_symphony = merged[merged["_merge"] == "left_only"]["url"].dropna().unique()
    solo_portfolio = merged[merged["_merge"] == "right_only"]["URL"].dropna().unique()
    em_ambos = merged[merged["_merge"] == "both"]["url"].dropna().unique()

    print("🔹 Solo en Symphony:", len(solo_symphony))
    print("🔹 Solo en Portfolio:", len(solo_portfolio))
    print("🔹 En ambos:", len(em_ambos))

    if len(merged) > 0:
        print("\n📋 Muestra del resultado:")
        print(merged.head(1).to_string(index=False))

except Exception as e:
    print(f"❌ Error al analizar resultados: {str(e)}")
    exit(1)

try:
    # --- 6. Exportar a Excel ---
    output_file = "Comparativo_Symphony_Portfolio.xlsx"
    merged.to_excel(output_file, index=False)
    print(f"\n✅ Comparación completada: {output_file}")

except Exception as e:
    print(f"❌ Error al exportar Excel: {str(e)}")
    print("💡 Verifica que no haya otro proceso usando el archivo")
    exit(1)

