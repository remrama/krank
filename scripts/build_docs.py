"""Generate corpora documentation pages from registry.yaml."""

from pathlib import Path

import yaml


DOCS_DIR = Path(__file__).parent.parent / "docs" / "corpora"
REGISTRY_PATH = Path(__file__).parent.parent / "src" / "krank" / "data" / "registry.yaml"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_template(name: str) -> str:
    template_path = TEMPLATES_DIR / name
    return template_path.read_text(encoding="utf-8")


def generate_corpus_page(name: str, entry: dict, versions: dict) -> str:
    """Generate markdown content for a single corpus."""
    template = load_template("corpus.md")
    
    latest = entry["latest"]
    version_info = versions[latest]
    
    # Build report fields table
    report_fields = entry.get("report_fields", [])
    report_fields_table = "\n".join(f"| `{field}` | |" for field in report_fields)
    
    # Build author fields table
    author_fields = entry.get("author_fields", [])
    author_fields_table = "\n".join(f"| `{field}` | |" for field in author_fields)
    
    # Build version table
    version_rows = []
    for version, info in sorted(versions.items(), reverse=True):
        short_hash = info.get("hash", "")[:20] + "..." if info.get("hash") else "N/A"
        version_rows.append(f"| {version} | `{short_hash}` |")
    version_table = "\n".join(version_rows)
    
    # Replace placeholders
    content = template
    replacements = {
        "{{ name }}": name,
        "{{ title }}": entry.get("title", "N/A"),
        "{{ description }}": entry.get("description", ""),
        "{{ n_reports }}": str(entry.get("n_reports", "N/A")),
        "{{ language }}": entry.get("language", "N/A"),
        "{{ license }}": entry.get("license", "N/A"),
        "{{ citation }}": entry.get("citation", "N/A"),
        "{{ source_url }}": entry.get("source_url", ""),
        "{{ download_url }}": version_info.get("download_url", ""),
        "{{ report_fields_table }}": report_fields_table,
        "{{ author_fields_table }}": author_fields_table,
        "{{ version_table }}": version_table,
    }
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    return content


def generate_index_page(corpora: dict) -> str:
    """Generate the corpora index page."""
    template = load_template("corpora_index.md")
    
    rows = []
    for name, entry in sorted(corpora.items()):
        desc = entry.get("description", "")[:50]
        if len(entry.get("description", "")) > 50:
            desc += "..."
        n_reports = entry.get("n_reports", "N/A")
        language = entry.get("language", "N/A")
        rows.append(f"| [{name}]({name}.md) | {desc} | {n_reports} | {language} |")
    
    corpora_table = "\n".join(rows)
    content = template.replace("{{ corpora_table }}", corpora_table)
    
    return content


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    registry = load_registry()
    corpora = registry.get("corpora", {})
    
    # Generate individual corpus pages
    for name, entry in corpora.items():
        versions = entry.get("versions", {})
        content = generate_corpus_page(name, entry, versions)
        output_path = DOCS_DIR / f"{name}.md"
        output_path.write_text(content, encoding="utf-8")
        print(f"Generated {output_path}")
    
    # Generate index page
    index_content = generate_index_page(corpora)
    index_path = DOCS_DIR / "index.md"
    index_path.write_text(index_content, encoding="utf-8")
    print(f"Generated {index_path}")


if __name__ == "__main__":
    main()
