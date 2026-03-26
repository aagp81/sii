# 🚀 Cómo Probar la Aplicación - Resumen Rápido

## ✅ Estado Actual
**¡La aplicación está FUNCIONANDO correctamente!**

- **Backend API**: http://localhost:5000 ✅
- **Frontend Web**: http://localhost:8080 ✅
- **Ambiente**: Pruebas (maquinaria.sii.cl) 🧪

---

## 🎯 3 Formas de Probar (Elige la que prefieras)

### Opción 1: Script Automático (Más Fácil) ⭐
```bash
cd /workspace/sii-dte-app/backend
source venv/bin/activate
python test_api.py
```
**Resultado**: Ejecuta 5 pruebas automáticas y muestra resultados

---

### Opción 2: Interfaz Web (Más Visual) 🌐
1. Abre tu navegador en: **http://localhost:8080**
2. Verás el dashboard del sistema DTE
3. Usa el formulario para crear facturas/boletas
4. Revisa la lista de documentos generados

---

### Opción 3: Comandos curl (Para Desarrolladores) 💻

#### Verificar estado:
```bash
curl http://localhost:5000/api/health
```

#### Generar factura:
```bash
curl -X POST http://localhost:5000/api/dte/generar \
  -H "Content-Type: application/json" \
  -d '{"tipo_documento": 33, "rut_receptor": "87654321-K", "razon_social_emisor": "Mi Empresa", "razon_social_receptor": "Cliente", "monto_neto": 100000, "iva": 19000, "monto_total": 119000}'
```

#### Listar documentos:
```bash
curl http://localhost:5000/api/dte/listar | python3 -m json.tool
```

---

## 📊 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Verificar estado |
| `/api/dte/generar` | POST | Crear DTE |
| `/api/dte/listar` | GET | Listar DTEs |
| `/api/dte/enviar/<id>` | POST | Enviar al SII |

---

## 📁 Archivos Importantes

- `GUIA_PRUEBAS.md` - Guía completa detallada
- `backend/test_api.py` - Script de pruebas automático
- `backend/.env` - Configuración actual
- `frontend/index.html` - Interfaz web

---

## 🔍 Tipos de Documentos que Puedes Probar

- **33**: Factura Electrónica
- **34**: Factura No Afecta (sin IVA)
- **39**: Boleta Electrónica
- **41**: Boleta Exenta
- **52**: Guía de Despacho
- **56**: Nota de Débito
- **61**: Nota de Crédito

---

## ⚠️ Importante

Esta aplicación está en **MODO PRUEBAS**:
- ✅ No requiere certificado digital real
- ✅ Los documentos NO tienen validez legal
- ✅ Usa el ambiente de pruebas del SII (maquinaria.sii.cl)

Para producción necesitarás:
1. Certificado digital autorizado
2. Folios electrónicos del SII
3. Certificación del sistema

---

## 🎉 ¡Listo para Usar!

La aplicación ya está corriendo. Solo elige un método y comienza a probar.

**¿Necesitas ayuda adicional?** Revisa `GUIA_PRUEBAS.md` para información detallada.
