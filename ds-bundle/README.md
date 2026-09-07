# reallife.network

Die Gestaltung von <https://reallife.network> — Landingpage und der
Real-Life-Stack-App darunter. Warmes Papier, vier Farben aus der
Knotengrafik, zwei Groteske.

## Setup

Kein Provider, kein Wrapper, keine Komponenten-Bibliothek: das hier ist
**CSS und Tokens**. Eine Seite braucht genau eine Zeile:

```html
<link rel="stylesheet" href="tokens/tokens.css">
```

Danach stehen alle Namen unten als `var(--*)` bereit — im Hellen wie im
Dunkeln, ohne weiteres Zutun. Schrift laden (`Bricolage Grotesque`,
`Hanken Grotesk`, `Spectral` kursiv) und `body` auf `var(--cream)` /
`var(--ink)` setzen; ohne einen gesetzten Hintergrund erbt die Seite den
des Wirts und kippt im Dunkelmodus.

## Zwei Ebenen, ein Satz Farben

`tokens/tokens.css` führt beides:

| Namen | Wofür |
|---|---|
| `--cream --surface --line --ink --body --muted --faint --outline` | Fläche und Schrift der **Landingpage** |
| `--forest --sage --ocker --terracotta --on-forest` | die **Marke** |
| `--band-bg --band-surface --band-line --band-text --band-body` | das dunkle **Band** (in jedem Schema dunkel) |
| `--background --foreground --card --primary --muted --accent --border --ring --warning --chart-1…5 --sidebar*` | die **App** — Tokens des Toolkits, aus `branding/theme.json` |

Die zweite Ebene ist keine zweite Palette: sie legt dieselben Farben auf die
Namen, die das Toolkit kennt. Ein Name, den das Toolkit nicht kennt, wird zur
Laufzeit verworfen und in der Konsole gemeldet.

**Jeder Name existiert in beiden Schemata.** Ein nur hell definierter Wert
wäre im Dunkeln ein Loch. Der Dunkelmodus kommt über
`prefers-color-scheme`; die App schaltet zusätzlich die Klasse `dark` am
Wurzelelement — beides ist bedient, und beides muss bedient bleiben.

## Form

| Token | Wert | Wofür |
|---|---|---|
| `--radius-control` | 13px | Knöpfe |
| `--radius-quest` | 14px | Einladungszeilen |
| `--radius-cta` | 16px | „Eintreten" |
| `--radius-tile` | 18px | Bildkacheln |
| `--radius-card` | 20px | Karten |
| `--radius-band` | 28px | Bänder, Einladungsfläche |
| `--radius-pill` | 999px | Auszeichnungen, Chips, Kopfzeilen-Knopf |
| `--shadow-tile` | 0 10px 30px rgba(42,40,32,.10) | **nur** Bildkacheln |

Karten und Bänder tragen keine Höhe: sie stehen auf der Fläche, nicht
darüber. Ränder sind durchgehend `1px solid var(--line)`, der zweitrangige
Knopf trägt `1.5px solid var(--outline)`.

## Schrift

`--font-display` (Bricolage Grotesque) für **jede** Überschrift und die
Wortmarke, `--font-sans` (Hanken Grotesk) für alles andere,
`--font-quote` (Spectral kursiv) für genau eine Stelle: das Zitat.

Alle Größen sind `clamp()`. Die obere Stufe: h1 60px/800/lh .96/ls −.035em ·
h2 46px/800/lh 1.02 · Vorspann 21px/lh 1.55 · Fließtext 16px/lh 1.6 ·
Kartentitel 21px/700 mit 15px/lh 1.55 darunter · Kicker 13px/700 versal mit
ls .14em · Kleingedrucktes 14.5px.

## Haltung

- **Einladen, nicht erklären.** Die Seite beschreibt nicht, was das Netz
  sei — sie fordert zum Mitmachen auf. Eine Hauptaktion je Fläche, mehrfach
  über die Seite wiederholt, nie drei konkurrierende Knöpfe nebeneinander.
- **Form vor Ornament.** Struktur entsteht aus Fläche, Farbe und Abstand.
  Wo anderswo ein Symbol stünde, steht hier ein farbiger Punkt oder Strich.
  Die Knotenmarke trägt nur das Favicon.
- **Nichts von Dritten.** Schriften und Bilder liegen bei uns. Wer die Seite
  öffnet, wird an keinen fremden Server gemeldet.

## Beispiel

```html
<section style="background: var(--surface); border: 1px solid var(--line);
                border-radius: var(--radius-band); padding: 64px 48px; text-align: center">
  <h2 style="font-family: var(--font-display); font-size: clamp(36px, 6vw, 58px);
             font-weight: 800; letter-spacing: -.03em; margin: 0">Mach mit!</h2>
  <p style="margin: 20px auto 32px; max-width: 30em; font-size: 20px;
            line-height: 1.55; color: var(--body); text-wrap: pretty">
    Du brauchst keine Erlaubnis und keinen Grund.
  </p>
  <a href="/app/" style="display: inline-block; background: var(--terracotta);
     color: #F6F1E7; border-radius: var(--radius-cta); padding: 18px 44px;
     font-size: 19px; font-weight: 700; text-decoration: none">Eintreten</a>
</section>
```

## Wo die Wahrheit liegt

`tokens/tokens.css` ist die einzige Quelle für Farben und Form — lies sie,
bevor du gestaltest. Die Karten unter `foundations/`, `components/` und
`patterns/` zeigen, wie die Namen zusammenwirken.

Erzeugt aus der laufenden Seite: `landing/index.html` (Palette der Seite)
und `branding/theme.json` (Tokens der App), im Repo
[real-life-org/reallife-network-instanz](https://github.com/real-life-org/reallife-network-instanz).
