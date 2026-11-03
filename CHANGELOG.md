# Changelog

## 1.0.0

- Einrichtung eines Cisco-Telefons über die Home-Assistant-Oberfläche.
- Aktion `cisco_popup.send_message` mit Titel, Nachricht und Template-Unterstützung.
- HTTP-Basic-Authentifizierung und Formularversand von CiscoIPPhoneText-XML.
- Behandlung von HTTP-/Cisco-Fehlern und Zeitüberschreitungen.
- Verarbeitung von Antworten unabhängig vom HTTP-Charset.
- Deutsche und englische Oberflächentexte.

Bestätigter Teststand (2026-11-03): Installation über HACS, Einrichtung über
Geräte & Dienste, erfolgreiches Laden und Popup-Versand aus Home Assistant 2026.10.4
an ein Cisco CP-9971. Der Empfang wurde am Telefon bestätigt. Umlaute,
Zeilenumbrüche und XML-Sonderzeichen wurden zusätzlich direkt am Telefon geprüft.
Lokale Protokolltests decken simulierte Erfolgs- und Fehlerantworten ab.
