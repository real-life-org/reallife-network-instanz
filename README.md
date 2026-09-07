# reallife.network — Instanz

Die Instanz hinter <https://reallife.network>: Landingpage auf `/`,
Real-Life-Stack-App auf `/app`. Es wird **nichts gebaut** — die App kommt als
fertiges Image aus `ghcr.io/real-life-org/rls-app`, alles hier ist
Konfiguration und Assets (siehe [Spec 11][spec] und `deploy/app/README.md` im
Stack-Repo).

[spec]: https://github.com/real-life-org/real-life-stack/blob/master/docs/spec/11-runtime-config-und-branding.md

## Was hier liegt

```
landing/      die Landingpage - freies HTML, wird auf / ausgeliefert
  fonts/      selbst gehostet, keine Anfrage an Dritte
  fotos/      sechs Bilder; vier davon zeigt die Seite je Besuch
branding/     theme.json (Farbtokens) und favicon.svg
docker-compose.yml
.env.example  Vorlage; die echte .env steht auf dem Server
```

## Betrieb

Verzeichnis auf dem Server: `/home/timo/apps/rls-app/`
(Host `h2980589.stratoserver.net`, Traefik + Let's Encrypt).

```bash
docker compose up -d      # liest .env, zieht das gepinnte Image
```

`landing/` und `branding/` sind **read-only gemountet**: eine geänderte Datei
wirkt beim nächsten Laden der Seite, ohne Neustart. Nur Änderungen an `.env`
brauchen ein erneutes `docker compose up -d`, weil daraus die `config.json`
der App entsteht.

**Wichtig beim Ausrollen:** Dateien *im* gemounteten Verzeichnis ersetzen,
das Verzeichnis selbst nicht löschen und neu anlegen — der laufende Container
zeigt sonst weiter auf das alte Inode und liefert 403.

## Abweichungen von der Vorlage im Stack-Repo

* `network_mode: bridge` statt eines externen `web`-Netzes: Traefik hängt auf
  diesem Server auf der Default-Bridge, wie alle anderen Apps dort.
* Eine Traefik-Regel schreibt `/app` auf `/app/` um. Das ist ein Übergang,
  bis das Image den Redirect selbst proxy-tauglich ausgibt
  (real-life-stack#296); danach kann sie raus.
* `watchtower.enable=false` — die Instanz pinnt ihre Version bewusst.

## Bilder

Sechs Bilder, vier Kacheln: drei quer, eine hoch. Ein kleines Skript in
`landing/index.html` zieht bei jedem Besuch neu, getrennt nach Format, damit
das Mosaik seine Form behält. Ohne JavaScript gilt die im Markup stehende
Auswahl.

Die Bilder sind auf rund das Doppelte ihrer Darstellungsgröße gerechnet und
als WebP abgelegt. Wer ein Bild austauscht, muss `width`/`height` im Markup
mitziehen, sonst springt die Seite beim Laden.

Alle abgebildeten Menschen haben zugestimmt.

## Schriften

`landing/fonts/` enthält Bricolage Grotesque, Hanken Grotesk und Spectral —
alle drei unter der [SIL Open Font License 1.1][ofl], die das Mitliefern
ausdrücklich erlaubt. Sie liegen bewusst hier statt bei Google: so lädt die
Seite keine Ressource von Dritten, und niemand wird beim Besuch an einen
fremden Server gemeldet.

[ofl]: https://openfontlicense.org/

## Bilder

Alle abgebildeten Menschen haben der Veröffentlichung zugestimmt.
