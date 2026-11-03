# Auf GitHub veröffentlichen

Vorgeschlagener Repository-Name: `cisco-popup`.

## 1. GitHub-Benutzernamen eintragen

Im Repository-Ordner ausführen (philipphunger ersetzen):

```sh
python scripts/configure_repository.py philipphunger
```

Das aktualisiert `documentation`, `issue_tracker` und `codeowners` im Manifest.
Die Metadaten sind bereits für `philipphunger/cisco-popup` eingetragen.

## 2. Repository hochladen

Auf GitHub ein leeres Repository `cisco-popup` anlegen. Den **Inhalt** dieses
Ordners hochladen, einschließlich `.github`, `.gitignore`, `LICENSE` und `hacs.json`.
`custom_components` muss direkt auf der obersten Repository-Ebene liegen.
Alternativ im entpackten Repository-Ordner:

```sh
git init -b main
git add .
git commit -m "Initial Cisco Popup integration"
git remote add origin https://github.com/philipphunger/cisco-popup.git
git push -u origin main
```

## 3. Prüfen und Release erstellen

- Den Workflow unter **Actions → Validate** prüfen.
- Vor einer stabilen Veröffentlichung die Installation und eine Nachricht in Home Assistant testen.
- Ein GitHub-Release mit Tag `v1.0.0` erstellen; die Integrationsversion steht im Manifest.
- Den Text aus `CHANGELOG.md` als Release-Beschreibung verwenden und auf den bisherigen Testumfang hinweisen.

HACS kann das Repository als benutzerdefinierte Integration nutzen.
Die Aufnahme in den Standardkatalog ist ein eigener Vorgang und hier nicht erfolgt.
