from pathlib import Path
import importlib.util
import json
import sys
root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("site_translate", root / "scripts/translate-site.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
blocks = json.loads((root / "src/i18n/te/blocks.json").read_text())
for source, value in blocks.items():
    module.validate_value(source, value)
metadata = json.loads((root / "src/i18n/te/news.json").read_text())
posts = json.loads((root / "src/data/news-posts.json").read_text())
for post in posts:
    translated = metadata[post["slug"]]
    html = (root / "src/i18n/te/news" / (post["slug"] + ".html")).read_text()
    module.news.validate_translation(post, {"title": translated["title"], "html": html})
    assert translated["sourceHash"] == module.news.source_hash(post)
print(f"PASS: {len(blocks)} prose blocks, {len(posts)} articles, all source hashes")
