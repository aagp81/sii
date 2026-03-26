# Sistema de Emisión DTE Chile

Aplicación web para la emisión electrónica de documentos tributarios (DTE) conectada al SII de Chile.

## 📋 Características

- ✅ Generación de Facturas Electrónicas (33, 34)
- ✅ Generación de Boletas Electrónicas (39, 41)
- ✅ Notas de Crédito y Débito (56, 61)
- ✅ Guías de Despacho (52)
- ✅ Firma digital de documentos XML
- ✅ Envío automático al SII
- ✅ Consulta de estado (ACE/RCV)
- ✅ Generación de PDFs
- ✅ Interfaz web moderna y responsiva

## 🚀 Instalación

### Requisitos Previos

1. Python 3.8 o superior
2. Certificado digital vigente (.p12 o .pem)
3. Folios electrónicos autorizados por el SII
4. RUT activo en el SII

### Paso 1: Clonar el repositorio

```bash
cd sii-dte-app
```

### Paso 2: Instalar dependencias del backend

```bash
cd backend
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

Crear archivo `.env` en la carpeta `backend`:

```env
RUT_EMPRESA=76000000-0
CERTIFICADO_PATH=ruta/al/certificado.p12
CERTIFICADO_PASSWORD=tu_password
AMBIENTE=PRUEBAS  # o PRODUCCION
PORT=5000
```

### Paso 4: Iniciar el backend

```bash
cd backend
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

### Paso 5: Abrir el frontend

Abrir el archivo `frontend/index.html` en tu navegador o servirlo con un servidor web:

```bash
# Opción con Python
cd frontend
python -m http.server 8080

# Luego abrir http://localhost:8080
```

## 📁 Estructura del Proyecto

```
sii-dte-app/
├── backend/
│   ├── app.py              # Aplicación Flask principal
│   ├── requirements.txt    # Dependencias de Python
│   ├── .env               # Variables de entorno
│   └── certificados/      # Certificados digitales
├── frontend/
│   ├── index.html         # Interfaz de usuario
│   ├── css/              # Estilos adicionales
│   └── js/               # Scripts JavaScript
├── docs/
│   └── informacion_sii.md # Documentación del SII
└── README.md
```

## 🔌 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verificar estado del servicio |
| POST | `/api/dte/generar` | Generar nuevo DTE |
| POST | `/api/dte/enviar/<id>` | Enviar DTE al SII |
| GET | `/api/dte/listar` | Listar todos los DTE |
| GET | `/api/dte/<id>/pdf` | Obtener PDF del DTE |
| POST | `/api/consultar/rcv` | Consultar RCV del SII |

## 📝 Ejemplo de Uso

### Generar una factura

```bash
curl -X POST http://localhost:5000/api/dte/generar \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_documento": 33,
    "rut_receptor": "76000000-0",
    "razon_social_receptor": "Empresa SPA",
    "monto_neto": 10000,
    "giro_receptor": "Servicios"
  }'
```

## ⚠️ Consideraciones Importantes

### Certificación SII

Antes de usar este sistema en producción:

1. **Obtén tu certificado digital** en una certificadora autorizada
2. **Solicita folios electrónicos** en www.sii.cl
3. **Realiza el proceso de certificación** con el SII
4. **Prueba en ambiente de pruebas** (maquinaria.sii.cl)

### Seguridad

- Nunca compartas tu certificado digital
- Mantén tus contraseñas seguras
- Usa HTTPS en producción
- Implementa autenticación de usuarios

### Legal

- Este software es una base para desarrollo
- Debes cumplir con toda la normativa del SII
- Responsable del uso: el desarrollador/empresa

## 🆘 Solución de Problemas

### Error de conexión con el SII

- Verifica que el certificado esté vigente
- Confirma que estás usando el ambiente correcto (PRUEBAS/PRODUCCION)
- Revisa los logs del servidor

### Error de firma XML

- Verifica el formato del certificado
- Asegúrate de tener las librerías criptográficas instaladas
- Revisa la password del certificado

## 📚 Recursos Adicionales

- [Documentación oficial del SII](https://www.sii.cl/servicios_online/1498-servicios-online.html)
- [Manual Técnico DTE](https://www.sii.cl/documentos/dte/manual_dte.pdf)
- [Ambiente de Pruebas SII](https://maquinaria.sii.cl/)

## 💰 Costos Estimados

| Concepto | Costo Anual |
|----------|-------------|
| Certificado Digital | $30.000 - $50.000 CLP |
| Dominio .cl | $15.000 CLP (opcional) |
| Hosting | $0 (planes gratuitos) |
| **Total** | **~$45.000 CLP** |

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

## 📞 Soporte

Para consultas técnicas sobre el SII:
- Email: contacto@sii.cl
- Teléfono: 600 200 0100

---

**Nota**: Este software es una implementación de referencia. El desarrollador es responsable de cumplir con todas las normativas vigentes del Servicio de Impuestos Internos de Chile.
