# 🧪 Guía Completa para Probar la Aplicación SII DTE

## ✅ Estado Actual
La aplicación está **CORRECTAMENTE INSTALADA Y FUNCIONANDO** en modo pruebas.

- **Backend**: ✅ Ejecutándose en `http://localhost:5000`
- **Modo**: 🧪 Ambiente de PRUEBAS (maquinaria.sii.cl)
- **Certificado**: 🔸 Modo simulación (no requiere certificado real)

---

## 📋 Opción 1: Probar con curl (Recomendado para desarrollo)

### 1. Verificar que el servicio esté activo
```bash
curl http://localhost:5000/api/health
```

**Respuesta esperada:**
```json
{
    "estado": "OK",
    "servicio": "SII DTE API",
    "ambiente": "pruebas",
    "fecha": "2024-..."
}
```

### 2. Generar una Factura Electrónica (Tipo 33)
```bash
curl -X POST http://localhost:5000/api/dte/generar \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_documento": 33,
    "rut_receptor": "87654321-K",
    "razon_social_emisor": "Mi Empresa SpA",
    "giro": "Servicios",
    "razon_social_receptor": "Cliente SPA",
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
  }'
```

**Respuesta esperada:**
```json
{
    "success": true,
    "dte_id": 1,
    "folio": 1,
    "mensaje": "DTE generado exitosamente"
}
```

### 3. Listar todos los DTE generados
```bash
curl http://localhost:5000/api/dte/listar | python3 -m json.tool
```

### 4. Enviar un DTE al SII (solo en ambiente de pruebas)
```bash
curl -X POST http://localhost:5000/api/dte/enviar/1
```

---

## 🌐 Opción 2: Probar con Interfaz Web

### Abrir el frontend directamente
1. Abre el archivo `/workspace/sii-dte-app/frontend/index.html` en tu navegador
2. La interfaz se conectará automáticamente al backend en `http://localhost:5000`

**Métodos alternativos:**

#### A) Usar Python HTTP Server
```bash
cd /workspace/sii-dte-app/frontend
python3 -m http.server 8080
```
Luego abre: `http://localhost:8080`

#### B) Usar Live Server en VS Code
1. Instala la extensión "Live Server" en VS Code
2. Haz clic derecho en `index.html`
3. Selecciona "Open with Live Server"

---

## 🧰 Opción 3: Usar Postman o Insomnia

### Colección de endpoints disponibles:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verificar estado del servicio |
| POST | `/api/dte/generar` | Generar nuevo DTE |
| GET | `/api/dte/listar` | Listar todos los DTE |
| POST | `/api/dte/enviar/<id>` | Enviar DTE al SII |
| GET | `/api/dte/<id>/pdf` | Obtener PDF del DTE |
| POST | `/api/consultar/rcv` | Consultar RCV |

### Ejemplo en Postman:

**Request: Generar Factura**
- Method: `POST`
- URL: `http://localhost:5000/api/dte/generar`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "tipo_documento": 33,
    "rut_receptor": "87654321-K",
    "razon_social_emisor": "Empresa Test",
    "giro": "Servicios",
    "razon_social_receptor": "Cliente Test",
    "monto_neto": 50000,
    "iva": 9500,
    "monto_total": 59500
}
```

---

## 🔧 Opción 4: Script de Prueba Automática

Crea un archivo `test_api.py`:

```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("🔍 Probando health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"✅ Status: {response.json()}")
    return response.status_code == 200

def test_generar_factura():
    print("\n📝 Generando factura...")
    data = {
        "tipo_documento": 33,
        "rut_receptor": "87654321-K",
        "razon_social_emisor": "Test SpA",
        "giro": "Servicios",
        "razon_social_receptor": "Cliente SpA",
        "monto_neto": 100000,
        "iva": 19000,
        "monto_total": 119000
    }
    response = requests.post(
        f"{BASE_URL}/api/dte/generar",
        json=data
    )
    print(f"✅ Resultado: {response.json()}")
    return response.status_code == 200

def test_listar():
    print("\n📋 Listando documentos...")
    response = requests.get(f"{BASE_URL}/api/dte/listar")
    data = response.json()
    print(f"✅ Total documentos: {data['total']}")
    return response.status_code == 200

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema DTE\n")
    
    tests = [
        test_health,
        test_generar_factura,
        test_listar
    ]
    
    resultados = []
    for test in tests:
        try:
            resultados.append(test())
        except Exception as e:
            print(f"❌ Error: {e}")
            resultados.append(False)
    
    print(f"\n{'='*50}")
    print(f"Resultados: {sum(resultados)}/{len(resultados)} pruebas exitosas")
    if all(resultados):
        print("🎉 ¡Todas las pruebas pasaron!")
    else:
        print("⚠️ Algunas pruebas fallaron")
```

Ejecutar:
```bash
cd /workspace/sii-dte-app/backend
source venv/bin/activate
python test_api.py
```

---

## 📊 Tipos de Documentos Disponibles para Prueba

| Código | Tipo de Documento | Uso |
|--------|------------------|-----|
| 33 | Factura Electrónica | Ventas afectas a IVA |
| 34 | Factura No Afecta | Ventas sin IVA |
| 39 | Boleta Electrónica | Ventas al público |
| 41 | Boleta Exenta | Ventas exentas |
| 52 | Guía de Despacho | Traslado de mercaderías |
| 56 | Nota de Débito | Aumentar monto de factura |
| 61 | Nota de Crédito | Anular/reducir monto |

---

## ⚙️ Configuración para Producción

Cuando tengas tu certificado digital real:

1. **Obtener certificado** en una certificadora autorizada
2. **Actualizar `.env`**:
   ```
   AMBIENTE=produccion
   CERTIFICADO_RUTA=/ruta/certificado.pfx
   CERTIFICADO_PASSWORD=tu_password
   MODO_SIMULACION=False
   ```

3. **Solicitar folios** en www.sii.cl
4. **Certificar el sistema** con el SII

---

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar logs
cat /workspace/sii-dte-app/backend/server.log

# Reiniciar servidor
cd /workspace/sii-dte-app/backend
source venv/bin/activate
python app.py
```

### Error de CORS
Asegúrate de que el frontend apunte a `http://localhost:5000`

### Puerto ya en uso
```bash
# Matar proceso
kill $(lsof -t -i:5000)

# O cambiar puerto en .env
FLASK_PORT=5001
```

---

## 📞 Endpoints de Prueba del SII

- **Ambiente Pruebas**: https://maquinaria.sii.cl
- **Ambiente Producción**: https://www.sii.cl
- **Documentación**: https://www.sii.cl/factura_electronica/documentacion.htm

---

## ✨ Próximos Pasos Recomendados

1. ✅ Probar generación de diferentes tipos de DTE
2. ✅ Implementar firma digital con certificado real
3. ✅ Agregar base de datos persistente (PostgreSQL)
4. ✅ Implementar generación de PDFs
5. ✅ Conectar con frontend interactivo
6. ✅ Certificar con el SII

---

**🎯 La aplicación está lista para usar en modo pruebas!**
