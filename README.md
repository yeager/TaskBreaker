# TaskBreaker

Bryt ner stora uppgifter till små, hanterbara mikrosteg.

Ett ADHD-anpassat verktyg byggt med GTK4/Adwaita.

## Funktioner

- Skriv in en uppgift (t.ex. "städa rummet")
- Får automatiskt konkreta mikrosteg
- Bocka av steg för steg med checkboxar
- Sparar dina uppgifter automatiskt
- Inbyggda mallar för vanliga uppgifter
- Tydlig, lugn design utan distraktion

## Installation

### Krav

- Python 3.10+
- GTK4 och libadwaita
- PyGObject

### Ubuntu/Fedora

```bash
# Ubuntu
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1

# Fedora
sudo dnf install python3-gobject gtk4 libadwaita

# Installera appen
pip install .
```

### Kör direkt

```bash
python -m taskbreaker.app
```

## Användning

1. Skriv in en uppgift i textfältet
2. Tryck Enter eller klicka "Bryt ner!"
3. Bocka av stegen ett i taget
4. Dina framsteg sparas automatiskt

## Inbyggda mallar

TaskBreaker känner igen vanliga uppgifter:
städa, diska, tvätta, laga mat, handla, plugga, träna, mejl

För okända uppgifter skapas generella steg.

## Licens

MIT
