# Notizen zum Design-System-Abgleich

Dieses Repo ist **kein Komponenten-Repo**: keine `package.json`, kein Build,
keine React-Komponenten. Die Landingpage ist statisches HTML mit Inline-Styles,
die App kommt als fertiges Image aus `real-life-stack`.

Der Konverter von `/design-sync` greift hier deshalb nicht — es gibt nichts zu
bündeln. Das Projekt in Claude Design ist von Hand erzeugt, in derselben
Bauform wie „Web of Trust": Tokens plus Vorschau-Karten mit `@dsCard`-Marker,
`"components": []`. Erzeugt wird es mit `scripts/` und den Quellen der Seite.

**Wenn irgendwann die echten Komponenten gebraucht werden** — damit der
Design-Agent mit ihnen bauen kann statt nur ihre Farben zu kennen — ist das
Ziel `real-life-stack/packages/toolkit`: dort liegen `.storybook/main.ts` und
114 Story-Dateien. Das ist ein eigener, mehrstündiger Erstimport in ein
eigenes Projekt, nicht dieses hier.

## Quellen

* `landing/index.html` — Palette und Maße der Seite
* `branding/theme.json` — die 32 Toolkit-Tokens je Schema (App unter `/app`)

Beide werden in `ds-bundle/tokens/tokens.css` zusammengeführt. Wer dort etwas
ändert, erzeugt das Bündel neu, statt die Karten von Hand nachzuziehen.
