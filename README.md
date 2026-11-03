# Cisco Popup

Eine benutzerdefinierte Home-Assistant-Integration für Text-Popups auf Cisco-IP-Telefonen.
Die Aktion `cisco_popup.send_message` lässt sich in Automationen und Skripten verwenden.
Ein Tastendruck am Telefon ist nicht erforderlich.

## Kompatibilität

Erfolgreich mit einem Cisco CP-9971 unter Home Assistant **2026.10.4** getestet.
Bestätigt sind die Installation über HACS, die Einrichtung über Geräte & Dienste
und der direkte Popup-Versand über `cisco_popup.send_message`. Der Empfang auf dem
Telefon wurde bestätigt. Umlaute, Zeilenumbrüche und XML-Sonderzeichen wurden
zusätzlich mit direkten Popup-Nachrichten am Telefon geprüft.
Andere Modelle und Firmwareversionen sind nicht getestet.
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
5. In einer Automation die Aktion `cisco_popup.send_message` verwenden.
   Eine Testnachricht unter **Werkzeuge / Entwicklerwerkzeuge → Aktionen** ist optional.

## HACS: benutzerdefiniertes Repository

1. In HACS unter **Benutzerdefinierte Repositories** die URL
   `https://github.com/philipphunger/cisco-popup` vom Typ **Integration** hinzufügen.
2. **Cisco Popup** herunterladen und Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen → Cisco Popup**
   die Telefon-IP und Zugangsdaten eintragen.
4. Die Aktion `cisco_popup.send_message` in einer Automation verwenden.

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
Formularversand, Antwortvalidierung und Zeitüberschreitungen. Ergänzend wurde der
reale Installations- und Versandweg unter Home Assistant 2026.10.4 erfolgreich
geprüft. Automatische Protokolltests decken weiterhin simulierte Fehlerfälle ab.

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
