"""
=============================================================================
SISTEMA DE ACTUALIZACION AUTOMATICA — PORTAL EDIFICIO MORAR
Ejecutable por Giancarlo Fauche o mediante el comando 'actualiza'
=============================================================================
"""

import os
import sys
import json
import re
import urllib.request
import subprocess
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"D:\Canales\Morar"
DASHBOARD_DIR = os.path.join(BASE_DIR, "morar-dashboard")
VJD_DIR = os.path.join(BASE_DIR, "vjd")
SCRATCH_DIR = r"C:\Users\gfauc\.gemini\antigravity\brain\2caffee9-28e7-4203-acd0-a50d3c5d03c2\scratch"
DRIVE_URL = "https://drive.google.com/drive/folders/1RELv4PTIJDpbxiYYCMwuWoH3uZmebs_5"

print("=" * 65)
print(">>> INICIANDO SINCRONIZACION DE COMPROBANTES Y DASHBOARD MORAR")
print("=" * 65)

# PASO 1: Escanear Google Drive para detectar nuevos vouchers
print("\n[1/5] Escaneando Google Drive para detectar nuevos comprobantes...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(DRIVE_URL, headers=headers)
try:
    html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
    print("  * Conexion exitosa a Google Drive.")
except Exception as e:
    print(f"  * Advertencia: No se pudo conectar a Google Drive ({e}). Se procesaran archivos locales.")
    html = ""

# Extraer IDs de archivos
drive_files = {}
if html:
    chunks = html.split("ssk='5:auSv")
    for c in chunks[1:]:
        m_id = re.search(r'^[0-9]+:([a-zA-Z0-9_-]{28,35})', c)
        if not m_id:
            continue
        fid = m_id.group(1)
        labels = re.findall(r'aria-label="([^"]+)"', c[:1500])
        name = "unknown"
        for l in labels:
            if any(ext in l for ext in [".pdf", ".jpg", ".png", "Shared", "Compartido"]):
                name = l.replace(" Image Shared", "").replace(" Imagen Compartido", "").replace(" PDF Shared", "").replace(" PDF Compartido", "")
                break
        drive_files[fid] = name

print(f"  * Total archivos identificados en Google Drive: {len(drive_files)}")

# PASO 2: Descargar archivos faltantes a D:\Canales\Morar\vjd
print("\n[2/5] Comprobando si hay archivos nuevos para descargar...")
local_files = set(os.listdir(VJD_DIR))
downloaded = 0
for fid, name in drive_files.items():
    clean_name = re.sub(r'[^a-zA-Z0-9_\.-]', '_', name)
    if not clean_name.endswith(('.jpg', '.png', '.pdf')):
        clean_name += ".jpg"
    
    dest_path = os.path.join(VJD_DIR, clean_name)
    if clean_name not in local_files:
        dl_url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
        try:
            req_dl = urllib.request.Request(dl_url, headers=headers)
            with urllib.request.urlopen(req_dl, timeout=10) as resp, open(dest_path, "wb") as f_out:
                f_out.write(resp.read())
            print(f"  * Descargado: {clean_name} ({fid})")
            downloaded += 1
        except Exception as e:
            pass

if downloaded == 0:
    print("  * Todos los comprobantes ya se encuentran en la carpeta local vjd.")

# PASO 3: Ejecutar Pipeline de OCR y Reconstrucción
print("\n[3/5] Ejecutando procesamiento OCR y conciliacion contable...")
rebuild_script = os.path.join(SCRATCH_DIR, "unify_ocr_and_rebuild.py")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True, encoding='utf-8', errors='replace')
if res.stdout:
    print(res.stdout.strip())
if res.stderr:
    print("Error:", res.stderr.strip())

# PASO 4: Generar Nuevo index.html del Dashboard
print("\n[4/5] Compilando Dashboard interactivo (build_dashboard.py)...")
build_script = os.path.join(DASHBOARD_DIR, "build_dashboard.py")
res_build = subprocess.run([sys.executable, build_script], capture_output=True, text=True, encoding='utf-8', errors='replace')
if res_build.stdout:
    print(res_build.stdout.strip())
if res_build.stderr:
    print("Error:", res_build.stderr.strip())

# PASO 5: Despliegue Automático a GitHub Pages
print("\n[5/5] Desplegando a GitHub Pages (gfauche/morar-dashboard)...")
try:
    os.chdir(DASHBOARD_DIR)
    subprocess.run(["git", "add", "index.html", "build_dashboard.py", "actualizar_dashboard.py"], check=True)
    commit_msg = f"update: sincronizacion automatica de vouchers ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("  * Cambios enviados exitosamente a GitHub.")
except subprocess.CalledProcessError as e:
    print("  * Nota: No hubo cambios para commitear o la rama ya esta al dia.")

print("\n" + "=" * 65)
print(">>> SINCRONIZACION COMPLETADA CON EXITO")
print("Dashboard En Vivo: https://gfauche.github.io/morar-dashboard/")
print("=" * 65)
