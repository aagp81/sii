#!/usr/bin/env python3
"""
Script de prueba para la API del sistema DTE - SII Chile
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("🔍 Probando health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"✅ Status: {response.json()}")
    return response.status_code == 200

def test_generar_factura():
    print("\n📝 Generando factura electrónica (Tipo 33)...")
    data = {
        "tipo_documento": 33,
        "rut_receptor": "87654321-K",
        "razon_social_emisor": "Test SpA",
        "giro": "Servicios de tecnología",
        "razon_social_receptor": "Cliente SpA",
        "monto_neto": 100000,
        "iva": 19000,
        "monto_total": 119000,
        "detalles": [
            {
                "cantidad": 1,
                "descripcion": "Servicio de consultoría",
                "precio_unitario": 100000,
                "monto_neto": 100000
            }
        ]
    }
    response = requests.post(
        f"{BASE_URL}/api/dte/generar",
        json=data
    )
    resultado = response.json()
    print(f"✅ Resultado: {json.dumps(resultado, indent=2)}")
    return response.status_code == 200 and resultado.get('success')

def test_generar_boleta():
    print("\n📝 Generando boleta electrónica (Tipo 39)...")
    data = {
        "tipo_documento": 39,
        "rut_receptor": "66666666-6",
        "razon_social_emisor": "Test SpA",
        "giro": "Comercio",
        "razon_social_receptor": "Consumidor Final",
        "monto_neto": 50000,
        "iva": 9500,
        "monto_total": 59500
    }
    response = requests.post(
        f"{BASE_URL}/api/dte/generar",
        json=data
    )
    resultado = response.json()
    print(f"✅ Resultado: {json.dumps(resultado, indent=2)}")
    return response.status_code == 200 and resultado.get('success')

def test_listar():
    print("\n📋 Listando documentos generados...")
    response = requests.get(f"{BASE_URL}/api/dte/listar")
    data = response.json()
    print(f"✅ Total documentos: {data['total']}")
    for doc in data['documentos']:
        print(f"   - ID: {doc['id']}, Tipo: {doc['tipo']}, Folio: {doc['folio']}, Monto: ${doc['monto']}")
    return response.status_code == 200

def test_enviar_sii():
    print("\n📤 Enviando documento al SII (solo pruebas)...")
    response = requests.post(f"{BASE_URL}/api/dte/enviar/1")
    resultado = response.json()
    print(f"✅ Resultado: {json.dumps(resultado, indent=2)}")
    return response.status_code == 200

def main():
    print("="*60)
    print("🚀 SISTEMA DE PRUEBAS - API DTE SII CHILE")
    print("="*60)
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Generar Factura", test_generar_factura),
        ("Generar Boleta", test_generar_boleta),
        ("Listar Documentos", test_listar),
        ("Enviar al SII", test_enviar_sii)
    ]
    
    resultados = []
    for nombre, test_func in tests:
        try:
            exito = test_func()
            resultados.append((nombre, exito))
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    for nombre, exito in resultados:
        estado = "✅ EXITOSA" if exito else "❌ FALLIDA"
        print(f"{estado} - {nombre}")
    
    exitos = sum(1 for _, e in resultados if e)
    total = len(resultados)
    
    print(f"\nTotal: {exitos}/{total} pruebas exitosas")
    
    if exitos == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON CORRECTAMENTE!")
        print("\n✨ La aplicación está funcionando correctamente.")
        print("📖 Para más detalles, revisa: GUIA_PRUEBAS.md")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisa los logs para más detalles.")
    
    print("="*60)

if __name__ == "__main__":
    main()
