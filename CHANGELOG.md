# Changelog

## 1.0.0

- Einrichtung eines Cisco-Telefons über die Home-Assistant-Oberfläche.
- Aktion `cisco_popup.send_message` mit Titel, Nachricht und Template-Unterstützung.
- HTTP-Basic-Authentifizierung und Formularversand von CiscoIPPhoneText-XML.
- Behandlung von HTTP-/Cisco-Fehlern und Zeitüberschreitungen.
- Verarbeitung von Antworten unabhängig vom HTTP-Charset.
- Deutsche und englische Oberflächentexte.

Testumfang: lokale Protokolltests; der entsprechende HTTP-Push wurde separat auf
einem CP-9971 getestet. Ein vollständiger HA-Installationstest steht noch aus.
