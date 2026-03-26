"""
Sistema de Emisión de DTE - Chile
Backend con Flask para integración con SII
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from lxml import etree
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
import requests
from zeep import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración
CERTIFICADO_PATH = os.getenv('CERTIFICADO_PATH', 'certificado.p12')
RUT_EMPRESA = os.getenv('RUT_EMPRESA', '')
AMBIENTE = os.getenv('AMBIENTE', 'PRODUCCION')  # PRODUCCION o PRUEBAS

# URLs del SII
if AMBIENTE == 'PRUEBAS':
    SII_WSDL_URL = "https://maquinaria.sii.cl/DTEWS/CrCertDTEService?wsdl"
    SII_ENVIO_URL = "https://maquinaria.sii.cl/DTEWS/ReceiveDTE"
else:
    SII_WSDL_URL = "https://www.sii.cl/DTEWS/CrCertDTEService?wsdl"
    SII_ENVIO_URL = "https://www.sii.cl/DTEWS/ReceiveDTE"

# Almacenamiento temporal en memoria (en producción usar base de datos)
dte_generados = []


def cargar_certificado(ruta_certificado, password):
    """Carga el certificado digital desde archivo .p12 o .pem"""
    with open(ruta_certificado, 'rb') as f:
        cert_data = f.read()
    
    # Implementar carga según formato
    # Esto es un ejemplo simplificado
    return cert_data


def firmar_xml(xml_string, certificado, clave_privada):
    """Firma un documento XML con certificado digital"""
    # Implementación simplificada de firma XML
    # En producción usar librería especializada como xmlsig
    
    hash_documento = hashlib.sha256(xml_string.encode()).digest()
    
    # Firmar hash con clave privada
    firma = clave_privada.sign(
        hash_documento,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    firma_b64 = base64.b64encode(firma).decode('utf-8')
    
    # Insertar firma en XML
    # Esto es pseudocódigo - implementar correctamente según esquema SII
    xml_firmado = xml_string.replace('</DTE>', f'<SignatureValue>{firma_b64}</SignatureValue></DTE>')
    
    return xml_firmado


def generar_dte(tipo_documento, datos):
    """Genera un DTE según tipo de documento"""
    
    # Estructura básica de DTE (simplificada)
    dte = {
        'Encabezado': {
            'TipoDTE': tipo_documento,
            'Folio': obtener_folio_disponible(tipo_documento),
            'FchEmis': datetime.now().strftime('%Y-%m-%d'),
            'RutEmisor': RUT_EMPRESA,
            'RutReceptor': datos['rut_receptor'],
            'MntNeto': datos.get('monto_neto', 0),
            'TasaIVA': 19,
            'Iva': datos.get('iva', 0),
            'MntTotal': datos.get('monto_total', 0),
        },
        'Emisor': {
            'RUTEmisor': RUT_EMPRESA,
            'RznSoc': datos.get('razon_social_emisor', ''),
            'GiroEmis': datos.get('giro', ''),
            'Acteco': datos.get('actividad_economica', ''),
            'DirOrigen': datos.get('direccion', ''),
            'CmnaOrigen': datos.get('comuna', ''),
        },
        'Receptor': {
            'RUTRecep': datos['rut_receptor'],
            'RznSocRecep': datos.get('razon_social_receptor', ''),
            'GiroRecep': datos.get('giro_receptor', ''),
            'DirRecep': datos.get('direccion_receptor', ''),
            'CmnaRecep': datos.get('comuna_receptor', ''),
        },
        'Detalles': datos.get('detalles', []),
    }
    
    return dte


def obtener_folio_disponible(tipo_documento):
    """Obtiene el siguiente folio disponible"""
    # En producción, esto debe venir de la base de datos
    # y estar sincronizado con los folios autorizados por el SII
    return 1


def convertir_a_xml(dte):
    """Convierte el DTE a formato XML según esquema SII"""
    
    # Ejemplo simplificado - en producción usar plantillas completas
    xml_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<DTE xmlns="http://www.sii.cl/SiiDte">
    <{obtener_tipo_documento_nombre(dte['Encabezado']['TipoDTE'])}>
        <Encabezado>
            <TipoDTE>{dte['Encabezado']['TipoDTE']}</TipoDTE>
            <Folio>{dte['Encabezado']['Folio']}</Folio>
            <FchEmis>{dte['Encabezado']['FchEmis']}</FchEmis>
            <RutEmisor>{dte['Encabezado']['RutEmisor']}</RutEmisor>
            <RutReceptor>{dte['Encabezado']['RutReceptor']}</RutReceptor>
            <MntNeto>{dte['Encabezado']['MntNeto']}</MntNeto>
            <TasaIVA>{dte['Encabezado']['TasaIVA']}</TasaIVA>
            <Iva>{dte['Encabezado']['Iva']}</Iva>
            <MntTotal>{dte['Encabezado']['MntTotal']}</MntTotal>
        </Encabezado>
        <Emisor>
            <RUTEmisor>{dte['Emisor']['RUTEmisor']}</RUTEmisor>
            <RznSoc>{dte['Emisor']['RznSoc']}</RznSoc>
            <GiroEmis>{dte['Emisor']['GiroEmis']}</GiroEmis>
        </Emisor>
        <Receptor>
            <RUTRecep>{dte['Receptor']['RUTRecep']}</RUTRecep>
            <RznSocRecep>{dte['Receptor']['RznSocRecep']}</RznSocRecep>
        </Receptor>
    </{obtener_tipo_documento_nombre(dte['Encabezado']['TipoDTE'])}>
</DTE>'''
    
    return xml_template


def obtener_tipo_documento_nombre(codigo):
    """Obtiene el nombre del tipo de documento según código"""
    tipos = {
        33: 'Factura',
        34: 'FacturaNoAfecta',
        39: 'Boleta',
        41: 'BoletaExenta',
        52: 'GuiaDespacho',
        56: 'NotaDebito',
        61: 'NotaCredito',
    }
    return tipos.get(codigo, 'Documento')


def enviar_al_sii(xml_firmado):
    """Envía el DTE firmado al SII"""
    try:
        # Crear cliente SOAP
        client = Client(SII_WSDL_URL)
        
        # Preparar envío
        respuesta = client.service.dteRecibir(
            rutEmisor=RUT_EMPRESA,
            ambiente=AMBIENTE,
            documento=xml_firmado
        )
        
        return {
            'estado': 'ENVIADO',
            'respuesta': respuesta,
            'fecha': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'estado': 'ERROR',
            'mensaje': str(e),
            'fecha': datetime.now().isoformat()
        }


@app.route('/api/dte/generar', methods=['POST'])
def generar_documento():
    """Endpoint para generar un DTE"""
    try:
        datos = request.json
        
        tipo_documento = datos.get('tipo_documento', 33)
        
        # Validar datos requeridos
        if 'rut_receptor' not in datos:
            return jsonify({'error': 'RUT receptor es requerido'}), 400
        
        # Generar DTE
        dte = generar_dte(tipo_documento, datos)
        
        # Convertir a XML
        xml_string = convertir_a_xml(dte)
        
        # Firmar documento (requiere certificado cargado)
        # xml_firmado = firmar_xml(xml_string, certificado, clave_privada)
        xml_firmado = xml_string  # Temporal sin firma
        
        # Guardar en almacenamiento
        dte_id = len(dte_generados) + 1
        dte_registro = {
            'id': dte_id,
            'tipo': tipo_documento,
            'folio': dte['Encabezado']['Folio'],
            'receptor': datos['rut_receptor'],
            'monto': dte['Encabezado']['MntTotal'],
            'fecha': datetime.now().isoformat(),
            'xml': xml_firmado,
            'estado': 'GENERADO'
        }
        dte_generados.append(dte_registro)
        
        return jsonify({
            'success': True,
            'dte_id': dte_id,
            'folio': dte_registro['folio'],
            'mensaje': 'DTE generado exitosamente'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dte/enviar/<int:dte_id>', methods=['POST'])
def enviar_documento(dte_id):
    """Endpoint para enviar DTE al SII"""
    try:
        # Buscar DTE
        dte = next((d for d in dte_generados if d['id'] == dte_id), None)
        
        if not dte:
            return jsonify({'error': 'DTE no encontrado'}), 404
        
        # Enviar al SII
        resultado = enviar_al_sii(dte['xml'])
        
        # Actualizar estado
        dte['estado'] = resultado['estado']
        dte['respuesta_sii'] = resultado
        
        return jsonify({
            'success': True,
            'resultado': resultado
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dte/listar', methods=['GET'])
def listar_documentos():
    """Lista todos los DTE generados"""
    return jsonify({
        'documentos': dte_generados,
        'total': len(dte_generados)
    })


@app.route('/api/dte/<int:dte_id>/pdf', methods=['GET'])
def obtener_pdf(dte_id):
    """Genera y retorna PDF del DTE"""
    # Implementar generación de PDF
    return jsonify({'mensaje': 'PDF en desarrollo'})


@app.route('/api/consultar/rcv', methods=['POST'])
def consultar_rcv():
    """Consulta el Registro de Ventas y Compras en el SII"""
    try:
        datos = request.json
        periodo = datos.get('periodo')  # Formato YYYYMM
        tipo_documento = datos.get('tipo_documento')
        
        # Implementar consulta al RCV del SII
        # Esto requiere autenticación con certificado
        
        return jsonify({
            'mensaje': 'Funcionalidad en desarrollo',
            'periodo': periodo,
            'tipo': tipo_documento
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado del servicio"""
    return jsonify({
        'estado': 'OK',
        'servicio': 'SII DTE API',
        'ambiente': AMBIENTE,
        'fecha': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
