import os
import re
import shutil
import zipfile
import requests
import time
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

URLS = [
    f"https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_{ano}.zip"
    for ano in range(1995, 2025)
]

PASTA_RAW = "data/raw"
PASTA_AUX = ".dev/aux_files"
PASTA_ZIPS = ".dev/zips"

PADRAO_CSV = re.compile(r".*\.csv$", re.IGNORECASE)
CHUNK_SIZE = 1024 * 1024
MAX_RETRIES = 3
MAX_WORKERS = 4

# Cria pastas
os.makedirs(PASTA_RAW, exist_ok=True)
os.makedirs(PASTA_AUX, exist_ok=True)
os.makedirs(PASTA_ZIPS, exist_ok=True)


def baixar_arquivo(url):
    #####  Baixa um ZIP com múltiplas tentativas e barra de progresso #####
    nome_arquivo = url.split("/")[-1]
    caminho_zip = os.path.join(PASTA_ZIPS, nome_arquivo)

    if os.path.exists(caminho_zip):
        return caminho_zip, f"🟡 {nome_arquivo} já existe — pulando download."

    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            with requests.get(url, stream=True, timeout=90) as r:
                r.raise_for_status()
                tamanho_total = int(r.headers.get("content-length", 0))
                progresso = tqdm(
                    total=tamanho_total,
                    unit="B",
                    unit_scale=True,
                    desc=f"⬇️ {nome_arquivo}",
                    leave=False,
                )

                with open(caminho_zip, "wb") as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            progresso.update(len(chunk))

                progresso.close()

            return caminho_zip, f"✅ Download concluído: {nome_arquivo}"

        except Exception as e:
            if tentativa < MAX_RETRIES:
                time.sleep(5)
            else:
                return None, f"❌ Falha ao baixar {nome_arquivo}: {e}"


def verificar_zip(caminho_zip):
    ##### Verifica integridade do arquivo ZIP #####
    try:
        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            erro = zip_ref.testzip()
            if erro is not None:
                raise zipfile.BadZipFile(f"Erro em {erro}")
        return True
    except Exception as e:
        print(f"⚠️  ZIP corrompido: {caminho_zip} ({e})")
        return False


def extrair_arquivos(caminho_zip):
    ##### Extrai arquivos do ZIP para pastas adequadas #####
    try:
        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            for nome_arquivo in zip_ref.namelist():
                if nome_arquivo.endswith("/"):
                    continue

                nome_base = os.path.basename(nome_arquivo)
                if not nome_base:
                    continue

                destino = (
                    os.path.join(PASTA_RAW, nome_base)
                    if PADRAO_CSV.fullmatch(nome_base)
                    else os.path.join(PASTA_AUX, nome_base)
                )

                extraido = zip_ref.extract(nome_arquivo, path=".tmp_extract")
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.move(extraido, destino)

        shutil.rmtree(".tmp_extract", ignore_errors=True)
        return f"📦 Extraído com sucesso: {os.path.basename(caminho_zip)}"

    except Exception as e:
        return f"❌ Erro ao extrair {caminho_zip}: {e}"


##### PIPELINE PRINCIPAL #####
def processar_zip(url):
    caminho_zip, msg_download = baixar_arquivo(url)
    print(msg_download)

    if not caminho_zip or not verificar_zip(caminho_zip):
        return f"🚫 Ignorado: {url}"

    msg_extracao = extrair_arquivos(caminho_zip)
    return msg_extracao


if __name__ == "__main__":
    print("🚀 Iniciando pipeline de download e extração do Censo Escolar")
    print(f"Total de anos: {len(URLS)}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = {executor.submit(processar_zip, url): url for url in URLS}
        for futuro in as_completed(futuros):
            print(futuro.result())

    print("\n🎉 Todos os downloads e extrações foram concluídos!")
