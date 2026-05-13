# 7 Colors of Souls — Manga Site

## Setup

```bash
pip install flask
python app.py
```

Site available at: http://localhost:5000

---

## Ajouter des pages au chapitre 1

Mets tes images dans:
```
manga/chapter_1/
  001.jpg
  002.jpg
  003.jpg
  ...
```

Les images doivent être nommées avec des numéros (001, 002...) pour garder l'ordre.
Formats supportés: .jpg .jpeg .png .webp

---

## Ajouter un nouveau chapitre

Dans app.py, ajoute une entrée dans le dictionnaire CHAPTERS:

```python
CHAPTERS = {
    'chapter_1': {
        'title': 'When the Journey Calls',
        'subtitle': 'Chapter 1 — The Beginning',
        'folder': 'chapter_1',
    },
    'chapter_2': {
        'title': 'Titre du chapitre 2',
        'subtitle': 'Chapter 2 — Subtitle',
        'folder': 'chapter_2',
    },
}
```

Puis crée le dossier `manga/chapter_2/` et mets tes images dedans.

---

## Deploy sur Render.com (gratuit)

1. Push le projet sur GitHub
2. Va sur render.com → New Web Service
3. Connecte ton repo GitHub
4. Start command: `python app.py`
5. Done — site en ligne gratuitement
