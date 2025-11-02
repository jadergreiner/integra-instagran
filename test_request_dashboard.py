#!/usr/bin/env python3
"""
Teste simples para fazer requisição com cookie ao dashboard
"""
import requests

# Token do teste E2E
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRlX2lkIjoxLCJlbWFpbCI6ImpvYW9AZW1wcmVzYS5jb20iLCJpYXQiOjE3NjIwNTQzMDQsImV4cCI6MTc2MjE0MDcwNCwidHlwZSI6ImNsaWVudGVfc2Vzc2lvbiJ9.ppyi3Gr87Gb7muWEOOIa1CzfpSTqhEp13BsTanz5aNc"

# Fazer requisição com cookie
cookies = {"client_token": token}

try:
    response = requests.get("http://127.0.0.1:8000/client/dashboard", cookies=cookies, allow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    if response.status_code == 302:
        print(f"Location: {response.headers.get('location')}")
    print(f"Content: {response.text[:500]}")
except Exception as e:
    print(f"Erro: {e}")