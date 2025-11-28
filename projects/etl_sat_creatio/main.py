import json
import pprint
from jsonpath_ng import jsonpath, parse
import requests
from pathlib import Path
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import middleware.creatio.tracking as tracking

load_dotenv()

session = requests.Session()

LOG_FILE = os.getenv("LOG_FILE")

# CERTS
CERTS_FOLDER = Path(os.getenv("CERTS_FOLDER"))
CER = next(CERTS_FOLDER.glob("*.cer"))
KEY = next(CERTS_FOLDER.glob("*.key"))

# SAT
URL_MASSIVE_DOWNLOAD = os.getenv("URL_MASSIVE_DOWNLOAD")
API_TOKEN = os.getenv("API_TOKEN")


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

# CREATIO
URL_AUTH_CREATIO = os.getenv("URL_AUTH_CREATIO")
URL_CREATIO = os.getenv("URL_CREATIO")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

HEADERS_CREATIO_AUTH = {
    "Content-Type": "application/x-www-form-urlencoded",
}

HEADERS_CREATIO = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "ForceUseSession": "true"
}

CREDENTIALS = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials"
}

count_tracking = 0


def extract_files(FORM_DATA):
    with open(CER, "rb") as cer, open(KEY, "rb") as key:
        files = {
            "cer": cer,
            "key": key
        }
        response = requests.post(URL_MASSIVE_DOWNLOAD,
                                 files=files, data=FORM_DATA, headers=HEADERS)
        return response


def ingest_data(rfc, pas, fecha_inicial, fecha_final, tipo_solicitud):
    log_process("*********************")
    log_process("Proceso de ingesta de datos iniciado")

    status_list = []

    FORM_DATA = {
        "rfc": str(rfc),
        "pas": str(pas),
        "fecha_inicial": datetime.fromisoformat(fecha_inicial),
        "fecha_final": datetime.fromisoformat(fecha_final),
        "tipo_solicitud": str(tipo_solicitud)
    }

    tracking.register_process()

    try:
        global count_tracking
        count_tracking = 0
        extracted_files = extract_files(FORM_DATA)
        if extracted_files.status_code != 200:
            message = f"Error en la extracción: Status code {extracted_files.status_code}, Response endpoint: {extracted_files.text}"
            log_process(message)
            tracking.register_status(message)
            tracking.register_final_tracking()
            status_list.append("SAT_NO_RESPONDE")
            raise Exception({"message": message, "status": status_list})

        tracking.register_status(f"{extracted_files.status_code}")
        extracted_status_code = extracted_files.status_code
        extracted_files = extracted_files.json()

    except Exception as e:
        message = f"Error al extraer los archivos cfdi. Detalles: {e}"
        log_process(message)
        tracking.register_status(message)
        tracking.register_final_tracking()
        status_list.append("SAT_NO_RESPONDE")
        raise Exception({"message": message, "status": status_list})

    conteo = extracted_files.get('conteo')
    if conteo is None:
        message = f"No se encontró la clave 'conteo': {extracted_files}"
        log_process(message)
        tracking.register_status(message)
        tracking.register_final_tracking()
        status_list.append("SAT_NO_RESPONDE")
        raise Exception({"message": message, "status": status_list})

    elif conteo == 0:
        message = "No hay archivos cfdi"
        log_process(message)
        tracking.register_status(message)
        tracking.register_final_tracking()
        status_list.append("SAT_NO_RESPONDE")
        raise Exception({"message": message, "status": status_list})
    else:
        log_process(f"Archivos extraidos: {conteo}")
        tracking.register_start_tracking(conteo)

    try:
        auth_creatio()
        log_process("Autenticación exitosa")
    except Exception as e:
        message = f"No se pudo autenticar: {e}"
        log_process(message)
        tracking.register_status(message)
        tracking.register_final_tracking()
        status_list.append("ERROR_ENVIO_CREATIO")
        raise Exception({"message": message, "status": status_list})

    status = extracted_files.get("estado_comprobante", "")
    request_type = extracted_files.get("tipo_solicitud", "")

    log_process("Proceso de mapeo campos iniciado")
    for cfdi in extracted_files['archivos']:
        try:
            match_properties(cfdi, status, request_type)
        except Exception as e:
            log_process(f"Error al procesar archivo cfdi. Detalles: {e}")
            status_list.append("ERROR_ENVIO_CREATIO")

    tracking.register_load(count_tracking)
    tracking.register_final_tracking()

    log_process("Proceso de mapeo campos terminado")
    log_process("Proceso de ingesta de datos terminado")
    log_process("*********************")

    if count_tracking == conteo:
        status_list.append("SINCRONIZADA_CORRECTAMENTE")
    else:
        status_list.append("SINCRONIZADA_INCOMPLETA")

    return f"{extracted_status_code}", status_list


def match_properties(cfdi, status, request_type):
    body = {}

    body["UsrVersionF66"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Version", 0))
    body["UsrUUIDF66"] = str(cfdi.get("xml_content", {}).get("cfdi_Comprobante", {}).get(
        "cfdi_Complemento", {}).get("tfd_TimbreFiscalDigital", {}).get("UUID", ""))

    set_concat_field(body, cfdi.get("xml_content", {}), "UsrUUIDrelacionadosF66", [
                     "cfdi_Comprobante", "cfdi_CfdiRelacionados", "cfdi_CfdiRelacionado", "UUID"])
    set_concat_field(body, cfdi.get("xml_content", {}), "UsrtiporelacionF77", [
                     "cfdi_Comprobante", "cfdi_CfdiRelacionados", "TipoRelacion"])

    body["UsrCPexpedicionF66"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("LugarExpedicion", 0))
    body["UsrSerieF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Serie", ""))
    body["UsrFolioF99"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante").get("Folio", ""))

    set_cfdi_type(body, cfdi)

    dt_emision = datetime.strptime(cfdi.get('xml_content', {}).get(
        'cfdi_Comprobante', {}).get('Fecha', "2000-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")
    body["UsrfechaemisionF66"] = dt_emision.replace(
        tzinfo=timezone.utc).isoformat()

    dt_certificacion = datetime.strptime(cfdi.get("xml_content", {}).get("cfdi_Comprobante", {}).get("cfdi_Complemento", {}).get(
        "tfd_TimbreFiscalDigital", {}).get("FechaTimbrado", "2000-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")
    body['UsrfechaCertificacionF66'] = dt_certificacion.replace(
        tzinfo=timezone.utc).isoformat()

    body["UsrpacCertificoF66"] = str(cfdi.get("xml_content", {}).get("cfdi_Comprobante", {}).get(
        "cfdi_Complemento", {}).get("tfd_TimbreFiscalDigital", {}).get("RfcProvCertif", ""))
    body["UsrregimenemisorF99"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Emisor", {}).get("RegimenFiscal", 0))
    body["UsrRFCemisorF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Emisor", {}).get("Rfc", ""))
    body["UsrrazonemisorF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Emisor", {}).get("Nombre", ""))
    body["UsrRFCReceptorF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Receptor", {}).get("Rfc", ""))
    body["UsrRazonReceptorF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Receptor", {}).get("Nombre", ""))
    body["UsrregimenreceptorF99"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Receptor", {}).get("RegimenFiscalReceptor", 0))
    body["UsrdomicilioreceptorF99"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Receptor", {}).get("DomicilioFiscalReceptor", 0))

    set_concat_field(body, cfdi.get("xml_content", {}), "UsrclavedeproductoF99", [
                     "cfdi_Comprobante", "cfdi_Conceptos", "cfdi_Concepto", "ClaveProdServ"])
    set_concat_field(body, cfdi.get("xml_content", {}), "UsrName", [
                     "cfdi_Comprobante", "cfdi_Conceptos", "cfdi_Concepto", "Descripcion"])
    set_concat_field(body, cfdi.get("xml_content", {}), "UsrcuentapredialF66", [
                     "cfdi_Comprobante", "cfdi_Conceptos", "cfdi_Concepto", "cfdi_CuentaPredial", "Numero"])

    body["UsrusoCFDIF99"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Receptor", {}).get("UsoCFDI", ""))
    body["UsrComplementosF66"] = str(cfdi.get("complemento", ""))
    body["UsrCondicionesdepagoF66"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("CondicionesDePago", ""))

    set_cfdi_status(body, status)
    set_request_type(body, request_type)

    body["UsrmonedaF99"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Moneda", ""))
    body["UsrtipodecambioF99"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("TipoCambio", 0))
    body["UsrExportacionF66"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Exportacion", 0))
    body["UsrmetododepagoF99"] = str(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("MetodoPago", ""))
    body["UsrformadepagoF99"] = int(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("FormaPago", 0))
    body["UsrSubtotalF66"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("SubTotal", 0))
    body["UsrdescuentoF66"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Descuento", 0))

    body["UsrIVAtrasladadoF66"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("cfdi_Impuestos", {}).get("TotalImpuestosTrasladados", 0))
    # es float en Creatio -> resultado -> "iva exento": "1818.75 | 5444.25"
    set_concat_field(body, cfdi.get("xml_content", {}), "UsrivaexentoF77", [
                     "cfdi_Comprobante", "cfdi_Impuestos", "cfdi_Traslados", "cfdi_Traslado", "Base"])

    set_retenciones(body, cfdi)

    body["UsrLocalTrasladoF66"] = float(cfdi.get("xml_content", {}).get("cfdi_Comprobante", {}).get(
        "cfdi_Complemento", {}).get("implocal_ImpuestosLocales", {}).get("implocal_TrasladosLocales", {}).get("Importe", 0))
    body["UsrTotalF66"] = float(cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("Total", {}))

    send_data(body)


def set_concat_field(body: dict, data, body_key: str, keys: list):
    def extract_value(d, keys):
        if not keys or d is None:
            return []
        key = keys[0]
        rest_keys = keys[1:]

        if isinstance(d, list):
            return [v for item in d for v in extract_value(item, keys)]

        elif isinstance(d, dict):
            if rest_keys:
                return extract_value(d.get(key), rest_keys)
            else:
                val = d.get(key)
                return [val] if val is not None else []
        else:
            return []

    values = extract_value(data, keys)

    values = [str(v) for v in values if v is not None]
    body[body_key] = " | ".join(values)


def set_cfdi_status(body, status):
    if status == "Vigente":
        body["UsrEstadoF66Id"] = "5034c41e-a2b8-424c-ba62-b413eb16668c"
    elif status == "Todos":
        body["UsrEstadoF66Id"] = "d06f26d9-27e1-4eab-9668-35c1892db1cf"


def set_cfdi_type(body, cfdi):
    cfdi_type = cfdi.get("xml_content", {}).get(
        "cfdi_Comprobante", {}).get("TipoDeComprobante", "")

    if cfdi_type == "I":
        body["UsrTipodecomprobanteF66Id"] = "4b466ba5-12cd-49dd-be3d-bf752693d6cf"
    elif cfdi_type == "E":
        body["UsrTipodecomprobanteF66Id"] = "1b17cf7c-143b-4164-9e65-d374767da359"
    elif cfdi_type == "T":
        body["UsrTipodecomprobanteF66Id"] = "10d1cdef-e3a6-4eff-a081-ce6f4703fc53"
    elif cfdi_type == "N":
        body["UsrTipodecomprobanteF66Id"] = "9652f60a-edb5-4dd4-872c-e58a76f02f68"
    elif cfdi_type == "P":
        body["UsrTipodecomprobanteF66Id"] = "daeb5479-a695-4ce0-828d-bb4c5d237c16"


def set_request_type(body, request_type):
    if request_type == "recibidos":
        body["UsrsolicitudF66Id"] = "f57b5083-7505-445a-8808-99a12d570111"
    elif request_type == "emitidos":
        body["UsrsolicitudF66Id"] = "7f25ecc4-9dea-4a60-a584-8dfa908afb77"


def set_retenciones(body, cfdi):
    comprobante = cfdi.get("xml_content", {}).get("cfdi_Comprobante", {})
    conceptos = comprobante.get("cfdi_Conceptos", {}).get("cfdi_Concepto", [])

    if not isinstance(conceptos, list):
        conceptos = [conceptos]

    for concepto in conceptos:
        impuestos = concepto.get("cfdi_Impuestos", {})
        retenciones = impuestos.get(
            "cfdi_Retenciones", {}).get("cfdi_Retencion", [])

        if not isinstance(retenciones, list):
            retenciones = [retenciones]

        for ret in retenciones:
            impuesto = ret.get("Impuesto")
            importe = float(ret.get("Importe", 0))

            if impuesto == "002":
                body["UsrIVARetenidoF66"] = importe
            elif impuesto == "001":
                body["UsrISRetenidoF66"] = importe


def auth_creatio():
    auth = session.post(URL_AUTH_CREATIO, data=CREDENTIALS,
                        headers=HEADERS_CREATIO_AUTH)

    if auth.status_code == 200:
        data = auth.json()
        token = data.get("access_token")
        HEADERS_CREATIO["Authorization"] = f"Bearer {token}"
    else:
        raise Exception(
            {"message": "ERROR", "status": ["ERROR_ENVIO_CREATIO"]})


def send_data(body):
    response = session.post(URL_CREATIO, json=body, headers=HEADERS_CREATIO)

    if response.status_code != 200 and response.status_code != 201:
        raise Exception(
            {"message": "ERROR", "status": ["ERROR_ENVIO_CREATIO"]})
    else:
        global count_tracking
        count_tracking += 1


def log_process(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp}  -  {message}\n")
