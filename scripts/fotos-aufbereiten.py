#!/usr/bin/env python3
"""Bereitet die Fotos der Landingpage auf und traegt sie in die Seite ein.

Der Bildbestand wechselt haeufig. Statt jedes Mal von Hand zuzuschneiden,
umzurechnen und drei Stellen im HTML nachzuziehen, macht das hier ein Lauf:

    python3 scripts/fotos-aufbereiten.py ~/workspace/workspace/fotos

Was passiert:

* Jedes Bild wird nach Seitenverhaeltnis als quer oder hoch eingeordnet.
* Es wird mittig auf das Format der Kachel beschnitten, auf rund das Doppelte
  der Darstellungsgroesse gerechnet und als WebP abgelegt - alles darueber
  waere verschenkte Ladezeit.
* Die Bildlisten im Skript der Landingpage werden zwischen den Markern
  ersetzt, ebenso die vier fest im Markup stehenden Kacheln (sie gelten,
  wenn kein JavaScript laeuft).
* Bilder, die nicht mehr im Quellordner liegen, werden aus der Auslieferung
  entfernt.

Namen und Alt-Texte stehen in `fotos.json`. Fehlt dort ein Eintrag, bekommt
das Bild einen unspezifischen Alt-Text - und der Lauf sagt es deutlich, denn
ein erfundener Alt-Text waere schlimmer als ein unspezifischer.
"""

import json
import os
import re
import subprocess
import sys
from PIL import Image, ImageOps

QUER = (500, 375)   # 4:3 - drei Kacheln
HOCH = (440, 590)   # 3:4 - eine Kachel
UNSPEZIFISCH = "Ein Eindruck aus dem Netzwerk."

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(WURZEL, "landing", "fotos")
SEITE = os.path.join(WURZEL, "landing", "index.html")
ZUORDNUNG = os.path.join(WURZEL, "fotos.json")


def slug(dateiname):
    """Stabiler Name aus dem Quelldateinamen - gleiche Datei, gleicher Name."""
    ohne = os.path.splitext(dateiname)[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", ohne).strip("-")


def js_text(wert):
    """Ein Wert, der sicher in einfachen Anfuehrungszeichen in JS steht."""
    return json.dumps(wert, ensure_ascii=True)


def main(quellordner):
    zuordnung = json.load(open(ZUORDNUNG, encoding="utf-8"))["bilder"]
    os.makedirs(ZIEL, exist_ok=True)

    quer, hoch, ohne_alt = [], [], []
    erzeugt = set()

    dateien = sorted(
        f for f in os.listdir(quellordner)
        if os.path.isfile(os.path.join(quellordner, f))
        and f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    )
    if not dateien:
        sys.exit(f"Keine Bilder in {quellordner}")

    for datei in dateien:
        pfad = os.path.join(quellordner, datei)
        try:
            bild = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")
        except Exception as fehler:
            print(f"  uebersprungen: {datei} ({fehler})")
            continue

        breit, hochkant = bild.size
        ist_hoch = hochkant > breit * 1.15
        groesse = HOCH if ist_hoch else QUER

        eintrag = zuordnung.get(datei, {})
        name = eintrag.get("name") or slug(datei)
        alt = eintrag.get("alt")
        if not alt:
            alt = UNSPEZIFISCH
            ohne_alt.append(datei)

        jpg = os.path.join(ZIEL, name + ".jpg")
        webp = os.path.join(ZIEL, name + ".webp")
        ImageOps.fit(bild, groesse, Image.LANCZOS).save(jpg, "JPEG", quality=92)
        subprocess.run(["cwebp", "-quiet", "-q", "82", jpg, "-o", webp], check=True)
        os.remove(jpg)

        erzeugt.add(name + ".webp")
        (hoch if ist_hoch else quer).append((name, alt))
        kb = os.path.getsize(webp) // 1024
        print(f"  {name:34s} {groesse[0]}x{groesse[1]} {'hoch' if ist_hoch else 'quer'}  {kb:3d} KB")

    if len(quer) < 3 or len(hoch) < 1:
        sys.exit(f"Zu wenig Bilder: {len(quer)} quer (mindestens 3), {len(hoch)} hoch (mindestens 1).")

    # Was nicht mehr im Quellordner liegt, verschwindet auch aus der Auslieferung.
    for vorhanden in sorted(os.listdir(ZIEL)):
        if vorhanden.endswith(".webp") and vorhanden not in erzeugt:
            os.remove(os.path.join(ZIEL, vorhanden))
            print(f"  entfernt: {vorhanden}")

    seite = open(SEITE, encoding="utf-8").read()

    # --- Bildlisten im Skript ---
    def liste(paare):
        return "\n".join(
            f"      [{js_text(n)}, {js_text(a)}]," for n, a in paare
        ).rstrip(",")

    block = (
        "    // BILDER-ANFANG (erzeugt von scripts/fotos-aufbereiten.py)\n"
        f"    var quer = [\n{liste(quer)}\n    ]\n"
        f"    var hoch = [\n{liste(hoch)}\n    ]\n"
        "    // BILDER-ENDE"
    )
    seite, anzahl = re.subn(
        r"    // BILDER-ANFANG.*?    // BILDER-ENDE",
        lambda _: block, seite, flags=re.S,
    )
    if anzahl != 1:
        sys.exit("Marker BILDER-ANFANG/-ENDE nicht genau einmal gefunden.")

    # --- Die vier Kacheln im Markup (gelten ohne JavaScript) ---
    def kachel(name, alt, form, zuerst=False):
        b, h = (HOCH if form == "hoch" else QUER)
        prio = ' fetchpriority="high"' if zuerst else ""
        alt_html = alt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        return (
            f'      <img class="kachel" data-form="{form}" src="/fotos/{name}.webp"'
            f' width="{b}" height="{h}"\n'
            f'          {prio} loading="eager" decoding="async"\n'
            f'           alt="{alt_html}">'
        )

    markup = (
        "    <!-- KACHELN-ANFANG (erzeugt von scripts/fotos-aufbereiten.py) -->\n"
        '    <div class="spalte">\n'
        + kachel(*quer[0], "quer", zuerst=True) + "\n"
        + kachel(*quer[1], "quer") + "\n"
        "    </div>\n"
        '    <div class="spalte spalte-versetzt">\n'
        + kachel(*hoch[0], "hoch") + "\n"
        + kachel(*quer[2], "quer") + "\n"
        "    </div>\n"
        "    <!-- KACHELN-ENDE -->"
    )
    seite, anzahl = re.subn(
        r"    <!-- KACHELN-ANFANG.*?    <!-- KACHELN-ENDE -->",
        lambda _: markup, seite, flags=re.S,
    )
    if anzahl != 1:
        sys.exit("Marker KACHELN-ANFANG/-ENDE nicht genau einmal gefunden.")

    open(SEITE, "w", encoding="utf-8").write(seite)

    print(f"\n  {len(quer)} quer, {len(hoch)} hoch — Seite aktualisiert.")
    if ohne_alt:
        print("\n  OHNE EIGENEN ALT-TEXT (bitte in fotos.json nachtragen):")
        for d in ohne_alt:
            print(f"    {d}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Aufruf: {sys.argv[0]} <quellordner>")
    main(os.path.expanduser(sys.argv[1]))
