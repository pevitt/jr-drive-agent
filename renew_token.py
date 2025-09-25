#!/usr/bin/env python3
"""
Script para renovar el token de Google Drive
"""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes necesarios
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def renew_google_token():
    """
    Renueva el token de Google Drive
    """
    creds = None
    token_path = 'credentials/token.json'
    credentials_path = 'credentials/credentials.json'
    
    # Cargar token existente si existe
    if os.path.exists(token_path):
        print("🔄 Cargando token existente...")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Si no hay credenciales válidas, renovar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expirado, renovando...")
            try:
                creds.refresh(Request())
                print("✅ Token renovado exitosamente!")
            except Exception as e:
                print(f"❌ Error renovando token: {e}")
                print("🔑 Necesitas reautenticarte manualmente...")
                return False
        else:
            print("🔑 No hay token válido, necesitas reautenticarte...")
            return False
    
    # Guardar el token renovado
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
    
    print("✅ Token guardado exitosamente!")
    
    # Probar la conexión
    try:
        from googleapiclient.discovery import build
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(pageSize=1).execute()
        print("✅ Conexión con Google Drive verificada!")
        return True
    except Exception as e:
        print(f"❌ Error verificando conexión: {e}")
        return False

if __name__ == '__main__':
    renew_google_token()
