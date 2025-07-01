import ctypes
import subprocess
import os
import time
import requests
import platform
import logging
import json
import urllib.request
import smtplib
import socket
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

API_KEY = "zzzzzxxxxxxxxxxyyyyyyyyykkkkkkkkkk"

# Ruta base (compatible con .exe de PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurar log a archivo
log_path = os.path.join(BASE_DIR, "atera_log.txt")
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def es_administrador():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def log_print(msg):
    print(msg)
    logging.info(msg)

def instalar_atera():
    try:
        subprocess.run(['where', 'AteraAgent.exe'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log_print("El programa ya está instalado.")
        return False
    except subprocess.CalledProcessError:
        pass  # No instalado, continúa

    log_print("Instalando cliente de Atera...")
    nombre_archivo = "atera_installer.msi"
    ruta = os.path.join(BASE_DIR, nombre_archivo)

    url = "http://atera.cloud-services.es/GetAgent/Windows/?cid=XXX&fid=YYYY&aid=ZZZZZZZZZZZZZZ"

    if not os.path.exists(ruta):
        log_print("Descargando instalador...")
        try:
            urllib.request.urlretrieve(url, ruta)
            log_print("Descarga completa.")
        except Exception as e:
            log_print(f"Error al descargar el instalador: {e}")
            return False

    try:
        subprocess.run(["msiexec", "/i", ruta, "/passive", "/norestart"], check=True)
        log_print("Instalación completada correctamente.")
    except subprocess.CalledProcessError as e:
        log_print(f"Error durante la instalación: {e}")
        return False

    time.sleep(10)
    return True

def send_error(cos_del_missatge):
    smtp_server = 'mail.XXX.XXXX-XXXXXX.es'
    smtp_port = 465
    password = 'XXXXXXXXXXXXXXX'
    remitent = 'XXXXXXXXXXXX@YYYYYYYYYYYYYYYY.es'

    msg = MIMEMultipart()
    msg['From'] = remitent
    msg['To'] = 'ZZZZZZZZZZ@YYYYYYYYYYYYYYYY.es'
    msg['Subject'] = 'Atera install error'

    msg.attach(MIMEText(cos_del_missatge, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as servidor:
            servidor.login(remitent, password)
            servidor.send_message(msg)
        print("Reporte enviado")
    except Exception as e:
        print("Fallo al enviar el reporte. Teléfono: 9999999999", e)

def obtener_serial():
    try:
        comando = 'powershell "Get-CimInstance -Class Win32_BIOS | Select-Object -ExpandProperty SerialNumber"'
        resultado = subprocess.check_output(comando, shell=True)
        return resultado.decode().strip()
    except Exception as e:
        log_print(f"Error al obtener serial: {e}")
        return "Error"

def info_red():
    nombre_host = socket.gethostname()
    try:
        ip_local = socket.gethostbyname(nombre_host)
    except socket.gaierror:
        ip_local = "No disponible"

    try:
        resultado = subprocess.run(
            ['powershell', '-Command', 'Invoke-RestMethod -Uri "https://api.ipify.org?format=text"'],
            capture_output=True, text=True, check=True
        )
        ip_publica = resultado.stdout.strip()
    except subprocess.CalledProcessError:
        ip_publica = "No disponible"

    return {
        "Host": nombre_host,
        "IP Local": ip_local,
        "IP Pública": ip_publica
    }

def renombrar_dispositivo(serial, nombre, email, tel, instalat):
    headers = {"X-Api-Key": API_KEY}
    idpeople = ""
    try:
        r = requests.get("https://app.atera.com/api/v3/agents?itemsInPage=50", headers=headers, timeout=10)
    except Exception as e:
        log_print(f"Error al conectar con Atera: {e}")
        return False

    log_print(f"HTTP {r.status_code} al obtener agentes")
    if r.status_code != 200:
        log_print(r.text)
        return False

    isnextpage = True
    while isnextpage:
        try:
            data = r.json()
            agents = data.get("items", []) if isinstance(data, dict) else data
        except Exception as e:
            log_print(f"Error al decodificar JSON: {e}")
            log_print(r.text)
            return False

        for item in agents:
            if item.get("VendorSerialNumber") == serial:
                idpeople = item.get("AgentID")
                isnextpage = False
                break

        if not data.get("nextLink"):
            isnextpage = False
        else:
            try:
                r = requests.get(data["nextLink"], headers=headers, timeout=10)
            except Exception as e:
                log_print(f"Error al seguir nextLink: {e}")
                return False

    if idpeople:
        campos = {
            "Usuario actual": nombre,
            "Email": email,
            "Telefono contacte": tel,
            "Fecha instalacion": date.today().isoformat()
        }

        for campo, valor in campos.items():
            try:
                res = requests.put(
                    f"https://app.atera.com/api/v3/customvalues/agentfield/{idpeople}/{campo}",
                    headers={**headers, "Content-Type": "application/json"},
                    json={"value": valor},
                    timeout=10
                )
            except Exception as e:
                log_print(f"Error actualizando campo {campo}: {e}")
                return False

        reporte = f"Ordenador Modificat:\nNombre: {nombre}\nEmail: {email}\nTeléfono: {tel}\nInstalat: {instalat}"
        for k, v in info_red().items():
            reporte += f"\n{k} -- {v}"
        send_error(reporte)
        return True
    else:
        log_print("No se encontró ningún agente con ese número de serie.")
        reporte = f"Nombre: {nombre}\nEmail: {email}\nTeléfono: {tel}\nInstalat: {instalat}"
        for k, v in info_red().items():
            reporte += f"\n{k} -- {v}"
        send_error(reporte)
        return False

def main():
    if not es_administrador():
        log_print("No estás ejecutando el programa con permisos de administrador. Por favor, vuelve a abrirlo como administrador para continuar.")
        input("\nPresiona Enter para salir...")
        return

    nombre = input("Nombre completo: ")
    email = input("Correo electrónico: ")
    tel = input("Teléfono: ")

    atera_instalado = instalar_atera()
    atera_estado = "Sí" if atera_instalado else "No"

    serial = obtener_serial()
    log_print(f"Serial detectado: {serial}")

    if renombrar_dispositivo(serial, nombre, email, tel, atera_estado):
        log_print("Dispositivo renombrado correctamente.")
    else:
        log_print("No se pudo actualizar el nombre en Atera.")

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_print(f"Error inesperado: {e}")
        input("\nPresiona Enter para salir...")
