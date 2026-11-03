# Cisco Popup

Eine benutzerdefinierte Home-Assistant-Integration für Text-Popups auf Cisco-IP-Telefonen.
Die Aktion `cisco_popup.send_message` lässt sich in Automationen und Skripten verwenden.
Ein Tastendruck am Telefon ist nicht erforderlich.

## Kompatibilität

Für das Cisco CP-9971 entwickelt. Der zugrunde liegende HTTP/XML-Push wurde auf
einem CP-9971 erfolgreich mit einem separaten PowerShell-Skript getestet.
Die Integration selbst ist noch nicht in einer laufenden Home-Assistant-Installation
verifiziert. Andere Modelle und Firmwareversionen sind nicht getestet.
Eine FRITZ!Box kann die Telefonie übernehmen; sie ist am Popup-Versand nicht beteiligt.

## Voraussetzungen

- Home Assistant erreicht das Telefon per HTTP auf Port 80.
- Der Webzugriff und XML-Push sind am Telefon verfügbar.
- Eine funktionierende `authenticationURL` ist am Telefon eingerichtet; der
  Authentifizierungsdienst akzeptiert die verwendeten Zugangsdaten.
- Ein Telefon pro Home-Assistant-Installation; IPv4-Adressen werden unterstützt.

Der Authentifizierungsdienst sollte Zugangsdaten und Zieltelefon prüfen.
Ein Dienst, der pauschal `AUTHORIZED` zurückgibt, erlaubt allen erreichbaren Clients
den XML-Push. Diese Integration installiert oder verändert keinen Authentifizierungsdienst.
HTTP überträgt Nachrichten und Basic-Auth unverschlüsselt im lokalen Netz.

## Manuell installieren

1. Den Ordner `custom_components/cisco_popup` nach
   `/config/custom_components/cisco_popup` kopieren.
2. Home Assistant neu starten.
3. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Cisco Popup** öffnen.
4. Telefon-IP und Zugangsdaten eingeben.
5. Unter **Werkzeuge / Entwicklerwerkzeuge → Aktionen** eine Testnachricht senden.

## HACS: benutzerdefiniertes Repository

Nach Veröffentlichung kann die Repository-URL in HACS als benutzerdefiniertes
Repository vom Typ **Integration** hinzugefügt werden. Anschließend Cisco Popup
herunterladen, Home Assistant neu starten und die Integration wie oben einrichten.
Das Projekt ist nicht als HACS-Standardrepository gelistet oder zertifiziert.

## Verwendung

In einer Automation unter **Dann → Aktion hinzufügen** nach **Cisco Popup** suchen.
Dieser YAML-Block ist eine einzelne Aktion, keine vollständige Automation:

```yaml
action: cisco_popup.send_message
data:
  title: Haushalt
  message: Die Waschmaschine ist fertig.
```

Templates sind ebenfalls möglich:

```yaml
action: cisco_popup.send_message
data:
  title: Home Assistant
  message: "Nachricht um {{ now().strftime('%H:%M') }}."
```

## Grenzen und Fehlerbehandlung

- Titel bis 100 Zeichen, Nachricht bis 4000 Zeichen. Darstellung und Sonderzeichen
  hängen von der Telefon-Firmware ab.
- Ein neues Popup kann die vorherige Anzeige ersetzen.
- Keine Warteschlange, automatische Ausblendung, Tonausgabe oder Lesebestätigung.
- Die Einrichtung speichert Daten ohne Test-Popup; erst die Aktion sendet eine Nachricht.
- HTTP- und Cisco-XML-Fehler werden als Aktionsfehler gemeldet. Cisco-Fehler 4
  weist auf die Authentifizierung hin.
- Antworten werden als Bytes gelesen, damit fehlerhafte HTTP-Zeichensatzangaben
  älterer Cisco-Firmware den Versand nicht als Auslesefehler erscheinen lassen.
- Zeitlimit: 15 Sekunden. Keine automatische Wiederholung, da die Nachricht bei
  einem Timeout bereits angezeigt worden sein kann.
- Zur Änderung der Telefon-IP oder Zugangsdaten die Integration entfernen und neu hinzufügen.

## Entwicklung

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Die Protokolltests verwenden simulierte Telefonantworten. Sie testen XML-Escaping,
Formularversand, Antwortvalidierung und Zeitüberschreitungen. Sie ersetzen keinen
vollständigen Home-Assistant-Integrationstest.

Vor dem ersten GitHub-Upload siehe [PUBLISHING.md](PUBLISHING.md).
Beiträge sind willkommen. Bitte Fehler mit Telefonmodell, Firmware, HA-Version
und bereinigtem Fehlertext melden, ohne Zugangsdaten oder private Konfigurationen.

## Entfernen

Integration in **Geräte & Dienste** löschen, den Ordner `custom_components/cisco_popup`
entfernen und Home Assistant neu starten. Automationen mit der Aktion vorher anpassen.

## Lizenz und Referenzen

MIT, siehe [LICENSE](LICENSE). Unabhängiges Projekt ohne Verbindung zu Cisco oder Home Assistant.

- [Home Assistant: Integrationsaktionen](https://contributors.home-assistant.io/core/integrations/actions/)
- [HACS: Integrationen veröffentlichen](https://hacs.dev/docs/publish/integration/)
