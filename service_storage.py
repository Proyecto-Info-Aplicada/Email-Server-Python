import requests

STORAGE_BASE_URL = "http://127.0.0.1:5000/pdf-storage"
TIMEOUT_SECONDS = 10

def get_storage_file(correlation_id: str) -> bytes:
    """
    Obtiene el archivo PDF del Storage Server usando el correlation_id.
    """
    url = f"{STORAGE_BASE_URL}/{correlation_id}"
    print(f"Solicitando PDF desde Storage Server: {url}")

    response = requests.get(url, timeout=TIMEOUT_SECONDS, stream=True)
    
    if response.status_code == 200:
        print(f"PDF obtenido correctamente ({len(response.content)} bytes)")
        return response.content
    else:
        error_msg = f"Error al obtener PDF ({response.status_code}): {response.text}"
        print(error_msg)
        raise RuntimeError(error_msg)
