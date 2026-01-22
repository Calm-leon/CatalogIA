# import os

# # Fuerza a trabajar offline
# os.environ["HF_HUB_OFFLINE"] = "1"

# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import os

# # Fuerza desactivar verificación SSL en toda la sesión de requests
# session = requests.Session()
# session.verify = False
# requests.packages.urllib3.disable_warnings()

# os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
# --- Ignorar verificación SSL temporal (solo para descargar el modelo) ---
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# --- Desactivar warnings de SSL e info extra ---
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# --- Librerías principales ---
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import torch

try:
    # --- Ruta absoluta y lectura segura de la imagen ---
    image_path = os.path.join(os.path.dirname(__file__), r"Fotos_de_Prueba\Foto Nereo Lopez.png")
    if not os.path.exists(image_path):
        # Buscar en data/Fotos/
        alt_path = os.path.join(os.path.dirname(__file__), r"..\data\Fotos\Foto Nereo Lopez.png")
        if os.path.exists(alt_path):
            image_path = alt_path
        else:
            raise FileNotFoundError(f"Imagen no encontrada en {image_path} ni en {alt_path}")

    image = Image.open(image_path).convert("RGB")
    print("✅ Imagen cargada correctamente")
except FileNotFoundError:
    print("❌ Error: Imagen no encontrada en la ruta especificada")
    print("💡 Coloca una imagen PNG/JPG en data/Fotos/ para probar el módulo IA")
    exit(1)
except Exception as e:
    print(f"❌ Error al cargar imagen: {str(e)}")
    exit(1)

# --- Detectar dispositivo ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"📊 Dispositivo detectado: {device}")

try:
    # --- Cargar modelo BLIP-2 desde Hugging Face (descarga inicial) ---
    processor = Blip2Processor.from_pretrained(
        "Salesforce/blip2-flan-t5-xl",
        trust_remote_code=True
    )
    model = Blip2ForConditionalGeneration.from_pretrained(
        "Salesforce/blip2-flan-t5-xl",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto"
    )
    print("✅ Modelo BLIP-2 cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar modelo: {str(e)}")
    print("💡 Verifica conexión a internet para primera ejecución")
    exit(1)

# --- Prompt para catalogación ---
prompt = (
    "Question: Describe briefly this photograph for bibliographic cataloging purposes. "
    "Mention people, objects, context, and possible relevant topics."
)

try:
    # --- Preparar inputs ---
    inputs = processor(image, prompt, return_tensors="pt").to(device)

    # --- Generar resultado ---
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        caption = processor.decode(generated_ids[0], skip_special_tokens=True)

    print("✅ Descripción generada correctamente")
except Exception as e:
    print(f"❌ Error durante procesamiento IA: {str(e)}")
    exit(1)

# --- Limpiar texto ---
def limpiar_texto(texto):
    palabras = texto.split()
    resultado = []
    for i, palabra in enumerate(palabras):
        if i == 0 or palabra != palabras[i - 1]:
            resultado.append(palabra)
    return " ".join(resultado)

try:
    caption_limpia = limpiar_texto(caption)
    print("\nResultado de la catalogación automática:\n")
    print(caption_limpia)
except Exception as e:
    print(f"❌ Error al procesar texto: {str(e)}")
    exit(1)
