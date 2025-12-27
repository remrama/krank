"""Generate corpora documentation pages from registry.yaml."""

from pathlib import Path
import re

import krank
import yaml


DOCS_DIR = Path(__file__).parent.parent / "docs" / "corpora"
REGISTRY_PATH = Path(__file__).parent.parent / "src" / "krank" / "data" / "registry.yaml"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_template(name: str) -> str:
    """Load a markdown template by name."""
    template_path = TEMPLATES_DIR / name
    return template_path.read_text(encoding="utf-8")


def generate_corpus_page(name: str, info: dict, versions: dict) -> str:
    """Generate markdown content for a single corpus."""
    template = load_template("corpus.md")
    
    available_versions = krank.list_versions(name)
    latest_version = available_versions[-1]
    corpus = krank.load(name, version=latest_version)

    latest = info["latest"]
    version_info = versions[latest]
    
    # Build version table
    def build_version_table() -> str:
        version_rows = []
        for version, info in sorted(versions.items(), reverse=True):
            version_str = version + " (latest)" if version == latest else version
            hash_ = info.get("hash")
            doi = info.get("doi")
            url = f"https://doi.org/{doi}"
            version_rows.append(f"| {version_str} | `{hash_}` | [`{doi}`]({url}) |")
        version_table = "\n".join(version_rows)
        return version_table

    def build_fields_table(author_or_reports: str) -> str:
        """Build a markdown table for author or reports fields.
        WARNING: This assumes all columns except for 'author' and 'report'
        are described in the registry yaml file. Another way to do it would be to pull
        columns directly from the corpus.authors and corpus.reports DataFrames. Avoids
        downloading the corpus just to build the docs, but may lead to inconsistencies.
        """
        assert author_or_reports in {"author", "report"}, "Must be 'author' or 'report'"
        DEFAULT_DESCRIPTIONS = {
            "age": "Reported age of author at time of report",
            "sex": "Reported sex of author at time of report",
        }
        descriptions = corpus.metadata.get("column_descriptions", {})
        all_columns = list(descriptions)
        descriptions.update(DEFAULT_DESCRIPTIONS)
        author_columns = corpus.metadata.get("author_columns", [])
        report_columns = [ col for col in all_columns if col not in author_columns ]
        columns = author_columns if author_or_reports == "author" else report_columns
        column_descriptions = {col: descriptions.get(col, "No description available") for col in columns}
        rows = [ f"| `{col}` | {desc} |" for col, desc in column_descriptions.items() ]
        table = "\n".join(rows)
        return table

    def get_citation_text():
        citations = info.get("citations", [])
        if not citations:
            return "N/A"
        text = "\n\n".join(f"- {cite}" for cite in citations)
        # Replace DOI links with markdown links
        # Use regex to find DOIs in the citations
        PATTERN = r"https?://(dx\.)?doi\.org/10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b"
        text = re.sub(PATTERN, lambda m: f"[{m.group(0)}]({m.group(0)})", text)
        return text


    replacements = {
        "{{ name }}": name,
        "{{ title }}": info.get("title", "N/A"),
        "{{ description }}": info.get("description", ""),
        "{{ environment }}": info.get("environment", "N/A"),
        "{{ probe }}": info.get("probe", "N/A"),
        "{{ doi }}": version_info.get("doi", "N/A"),
        "{{ source_url }}": info.get("source_url", ""),
        "{{ download_url }}": version_info.get("download_url", ""),
        "{{ citation_text }}": get_citation_text(),
        "{{ report_columns_table }}": build_fields_table("report"),
        "{{ author_columns_table }}": build_fields_table("author"),
        "{{ version_table }}": build_version_table(),
        "{{ n_reports }}": str(len(corpus.reports)),
        "{{ n_authors }}": str(len(corpus.authors)),
        "{{ m_report_length }}": f"{corpus.reports["report"].str.split().apply(len).mean():.0f}",
        "{{ mdn_report_length }}": f"{corpus.reports["report"].str.split().apply(len).median():.0f}",
    }

    content = template
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
        corpus = krank.load(name, version=entry["latest"])
        n_reports = len(corpus.reports)
        n_authors = len(corpus.authors)
        probe = entry.get("probe", "N/A")
        environment = entry.get("environment", "N/A")
        name_linked = f"[{name}]({name}.md)"
        row = f"| {name_linked} | {desc} | {environment} | {probe} | {n_reports} | {n_authors} |"
        rows.append(row)
    
    corpora_table = "\n".join(rows)
    content = template.replace("{{ corpora_table }}", corpora_table)
    
    return content


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    registry = krank._registry.load_registry()
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
