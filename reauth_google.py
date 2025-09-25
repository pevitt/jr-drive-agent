#!/usr/bin/env python3
"""
Script para reautenticación completa con Google Drive
"""
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes necesarios
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def reauth_google():
    """
    Realiza reautenticación completa con Google Drive
    """
    credentials_path = 'credentials/credentials.json'
    token_path = 'credentials/token.json'
    
    if not os.path.exists(credentials_path):
        print(f"❌ No se encontró el archivo {credentials_path}")
        print("📁 Asegúrate de tener el archivo credentials.json en la carpeta credentials/")
        return False
    
    print("🔑 Iniciando proceso de reautenticación...")
    print("📋 Se abrirá una ventana del navegador para autenticarte")
    
    try:
        # Crear el flujo de autenticación
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES)
        
        # Ejecutar el flujo de autenticación
        creds = flow.run_local_server(port=0)
        
        print("✅ Autenticación exitosa!")
        
        # Guardar las credenciales
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
        print(f"💾 Credenciales guardadas en {token_path}")
        
        # Probar la conexión
        print("🔍 Probando conexión con Google Drive...")
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=1).execute()
        
        print("✅ Conexión con Google Drive verificada!")
        print(f"📊 Archivos en Drive: {len(results.get('files', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la autenticación: {e}")
        return False

if __name__ == '__main__':
    reauth_google()
