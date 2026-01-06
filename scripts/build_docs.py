"""Generate corpora documentation pages from registry.yaml.

This script automatically generates markdown documentation pages for each corpus
in the registry, including metadata, version information, field descriptions,
and summary statistics. It also generates an index page listing all corpora.
"""

import re
import shutil
from pathlib import Path

import krank

DOCS_DIR = Path(__file__).parent.parent / "docs" / "corpora"
SOURCES_DIR = Path(__file__).parent.parent / "sources"
REGISTRY_PATH = (
    Path(__file__).parent.parent / "src" / "krank" / "data" / "registry.yaml"
)
TEMPLATES_DIR = Path(__file__).parent / "templates"

def load_template(name: str) -> str:
    """Load a markdown template by name.

    Parameters
    ----------
    name : str
        Name of the template file to load (e.g., 'corpus.md').

    Returns
    -------
    str
        Contents of the template file.
    """
    template_path = TEMPLATES_DIR / name
    return template_path.read_text(encoding="utf-8")


def generate_corpus_page(name: str, info: dict, versions: dict) -> str:
    """Generate markdown content for a single corpus.

    Parameters
    ----------
    name : str
        Name of the corpus.
    info : dict
        Dictionary containing corpus metadata.
    versions : dict
        Dictionary mapping version strings to version-specific information.

    Returns
    -------
    str
        Formatted markdown content for the corpus documentation page.
    """
    template = load_template("corpus.md")

    available_versions = krank.list_versions(name)
    latest_version = available_versions[-1]
    corpus = krank.load(name, version=latest_version)

    latest = info["latest"]
    version_info = versions[latest]

    # Build version table
    def build_version_table() -> str:
        """Build a markdown table listing all versions.

        Returns
        -------
        str
            Markdown table with version, hash, and DOI information.
        """
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

        Parameters
        ----------
        author_or_reports : str
            Either 'author' or 'report' to specify which fields to document.

        Returns
        -------
        str
            Markdown table listing field names and descriptions.

        Notes
        -----
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
        report_columns = [col for col in all_columns if col not in author_columns]
        columns = author_columns if author_or_reports == "author" else report_columns
        column_descriptions = {
            col: descriptions.get(col, "No description available") for col in columns
        }
        rows = [f"| `{col}` | {desc} |" for col, desc in column_descriptions.items()]
        table = "\n".join(rows)
        return table

    def get_citation_text():
        """Extract and format citation text from corpus metadata.

        Returns
        -------
        str
            Formatted citation text with DOI links converted to markdown format.
        """
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
        "{{ brief_description }}": info.get("brief_description", ""),
        "{{ long_description }}": info.get("long_description", ""),
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
        "{{ m_report_length }}": f"{corpus.reports['report'].str.split().apply(len).mean():.0f}",
        "{{ mdn_report_length }}": f"{corpus.reports['report'].str.split().apply(len).median():.0f}",
    }

    content = template
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content


def generate_index_page(corpora: dict) -> str:
    """Generate the corpora index page.

    Parameters
    ----------
    corpora : dict
        Dictionary mapping corpus names to their metadata.

    Returns
    -------
    str
        Formatted markdown content for the corpora index page.
    """
    template = load_template("corpora_index.md")

    rows = []
    for name, entry in sorted(corpora.items()):
        desc = entry["brief_description"][:50]
        if len(entry["brief_description"]) > 50:
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
    """Generate all corpus documentation pages from registry.

    Creates individual markdown pages for each corpus and an index page
    listing all available corpora. Output is written to the docs/corpora directory.
    """
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
    
    # Copy individual processing notebooks
    for name, entry in corpora.items():
        source_notebook = SOURCES_DIR / name / "prepare.ipynb"
        target_notebook = DOCS_DIR / "notebooks" / name / "prepare.ipynb"
        target_notebook.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_notebook, target_notebook)

    # Generate index page
    index_content = generate_index_page(corpora)
    index_path = DOCS_DIR / "index.md"
    index_path.write_text(index_content, encoding="utf-8")
    print(f"Generated {index_path}")


if __name__ == "__main__":
    main()
