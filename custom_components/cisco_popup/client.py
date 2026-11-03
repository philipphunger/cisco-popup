"""Send Cisco XML popups using the phone's HTTP interface."""
import asyncio
from xml.etree import ElementTree as ET

from aiohttp import BasicAuth, ClientError, ClientTimeout


class PopupError(Exception):
    """The phone did not accept the popup."""


def message_xml(title: str, message: str) -> str:
    """Escape user text, including XML special characters."""
    for text in (title, message):
        if any(not (c in "\t\n\r" or 0x20 <= ord(c) <= 0xD7FF
                    or 0xE000 <= ord(c) <= 0xFFFD
                    or 0x10000 <= ord(c) <= 0x10FFFF) for c in text):
            raise PopupError("Der Text enthaelt ungueltige XML-Steuerzeichen.")
    root = ET.Element("CiscoIPPhoneText")
    ET.SubElement(root, "Title").text = title
    ET.SubElement(root, "Text").text = message
    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")


def check_response(status: int, raw: bytes) -> None:
    """Ignore the phone's potentially invalid HTTP charset header."""
    if status != 200:
        raise PopupError(f"Telefon meldet HTTP {status}.")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as err:
        raise PopupError("Keine gueltige Cisco-XML-Antwort vom Telefon.") from err
    if root.tag == "CiscoIPPhoneError":
        number = root.get("Number", "unbekannt")
        hint = " Authentifizierungs-URL und Zugangsdaten pruefen." if number == "4" else ""
        raise PopupError(f"Cisco-Fehler {number}.{hint}")
    if root.tag != "CiscoIPPhoneResponse":
        raise PopupError("Unerwartete Antwort vom Telefon.")
    items = list(root.iter("ResponseItem"))
    if not items or any(item.get("Status") != "0" for item in items):
        raise PopupError("Das Telefon hat die Nachricht nicht bestaetigt.")


async def send_popup(session, host, username, password, title, message):
    """POST form-encoded XML; never retry and accidentally duplicate a popup."""
    xml = message_xml(title, message)
    try:
        async with session.post(
            f"http://{host}/CGI/Execute",
            data={"XML": xml},
            auth=BasicAuth(username, password),
            timeout=ClientTimeout(total=15),
            allow_redirects=False,
        ) as response:
            raw = await response.read()
            check_response(response.status, raw)
    except (ClientError, asyncio.TimeoutError) as err:
        raise PopupError("Telefon nicht erreichbar oder Zeitlimit ueberschritten.") from err
