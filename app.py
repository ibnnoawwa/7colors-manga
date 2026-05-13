from flask import Flask, render_template, abort, send_from_directory
import os

app = Flask(__name__)

MANGA_DIR = os.path.join(os.path.dirname(__file__), 'manga')

MANGA_INFO = {
    'title': '7 Colors of Souls',
    'tagline': 'An original manga',
}

CHAPTERS = {
    'chapter_1': {
        'title': 'When the Journey Calls',
        'subtitle': 'Chapter 1 — The Beginning',
        'folder': 'chapter_1',
    }
}

COVER_NAMES = ['cover', 'cover.jpg', 'cover.jpeg', 'cover.png', 'cover.webp']

def find_cover(folder_path):
    if not os.path.exists(folder_path):
        return None
    files_lower = {f.lower(): f for f in os.listdir(folder_path)}
    for name in COVER_NAMES:
        if name in files_lower:
            return files_lower[name]
    return None

def get_pages(chapter_folder):
    path = os.path.join(MANGA_DIR, chapter_folder)
    if not os.path.exists(path):
        return []
    exts = ('.jpg', '.jpeg', '.png', '.webp')
    cover = (find_cover(path) or '').lower()
    files = sorted([
        f for f in os.listdir(path)
        if f.lower().endswith(exts) and f.lower() != cover
    ])
    return files

def chapter_has_cover(chapter_folder):
    return find_cover(os.path.join(MANGA_DIR, chapter_folder)) is not None

def manga_has_cover():
    return find_cover(MANGA_DIR) is not None

def get_manga_cover():
    return find_cover(MANGA_DIR)

def get_chapter_cover(chapter_folder):
    return find_cover(os.path.join(MANGA_DIR, chapter_folder))

@app.route('/')
def index():
    chapters = []
    for key, data in CHAPTERS.items():
        pages = get_pages(data['folder'])
        chapters.append({
            'key': key,
            'title': data['title'],
            'subtitle': data['subtitle'],
            'pages': len(pages),
            'has_cover': chapter_has_cover(data['folder']),
            'cover_file': get_chapter_cover(data['folder']),
        })
    return render_template('index.html',
        chapters=chapters,
        manga=MANGA_INFO,
        has_manga_cover=manga_has_cover(),
        manga_cover_file=get_manga_cover(),
    )

@app.route('/read/<chapter_key>')
def reader(chapter_key):
    if chapter_key not in CHAPTERS:
        abort(404)
    data = CHAPTERS[chapter_key]
    pages = get_pages(data['folder'])
    if not pages:
        abort(404)
    chapter_keys = list(CHAPTERS.keys())
    idx = chapter_keys.index(chapter_key)
    prev_chapter = chapter_keys[idx - 1] if idx > 0 else None
    next_chapter = chapter_keys[idx + 1] if idx < len(chapter_keys) - 1 else None
    cover_file = get_chapter_cover(data['folder'])
    return render_template('reader.html',
        chapter_key=chapter_key,
        chapter=data,
        pages=pages,
        has_cover=cover_file is not None,
        cover_file=cover_file,
        prev_chapter=prev_chapter,
        next_chapter=next_chapter,
    )

@app.route('/manga/<path:filepath>')
def manga_image(filepath):
    directory = os.path.dirname(os.path.join(MANGA_DIR, filepath))
    filename = os.path.basename(filepath)
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)
