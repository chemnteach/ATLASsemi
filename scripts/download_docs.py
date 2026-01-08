"""
Document Downloader for ATLASsemi RAG

Downloads public PDFs and HTML pages, organizes into reference_docs/ folders,
and converts HTML to markdown for consistent processing.

Usage:
    python scripts/download_docs.py docs_to_download.yaml

Input file format (YAML):
    methodologies:
      - url: https://example.com/8d-handbook.pdf
        name: 8d_handbook.pdf
      - url: https://example.com/dmaic-guide.html
        name: dmaic_guide.md

    yield:
      - url: https://example.com/spc-manual.pdf
        name: spc_manual.pdf

Or simple text format (one per line):
    methodologies: https://example.com/8d-handbook.pdf
    yield: https://example.com/spc-manual.pdf
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote
import requests
from typing import Dict, List, Tuple
import re


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 200:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:190] + (f'.{ext}' if ext else '')
    return filename


def guess_filename_from_url(url: str, content_type: str = None) -> str:
    """Guess filename from URL or content type."""
    # Try to get filename from URL path
    parsed = urlparse(url)
    path = unquote(parsed.path)
    filename = Path(path).name

    if filename and '.' in filename:
        return sanitize_filename(filename)

    # Fallback: generate from URL
    domain = parsed.netloc.replace('www.', '')
    name = domain.split('.')[0] + '_' + path.replace('/', '_').strip('_')

    # Add extension based on content type
    if content_type:
        if 'pdf' in content_type:
            name += '.pdf'
        elif 'html' in content_type:
            name += '.html'
        else:
            name += '.txt'
    else:
        name += '.pdf'  # Default assumption

    return sanitize_filename(name)


def download_file(url: str, output_path: Path) -> bool:
    """
    Download file from URL to output path.

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Downloading: {url}")
        response = requests.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)

        print(f"  ✓ Saved to: {output_path}")
        return True

    except requests.RequestException as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False


def html_to_markdown(html_content: str, url: str) -> str:
    """
    Convert HTML to markdown.

    Uses html2text library if available, otherwise basic conversion.
    """
    try:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # Don't wrap lines
        markdown = h.handle(html_content)

        # Add source URL at top
        header = f"# Document from {url}\n\n---\n\n"
        return header + markdown

    except ImportError:
        # Fallback: basic HTML stripping
        print("  Note: html2text not installed, using basic conversion")
        print("  Install for better results: pip install html2text")

        from html.parser import HTMLParser

        class HTMLToText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False

            def handle_starttag(self, tag, attrs):
                if tag in ['script', 'style', 'meta', 'link']:
                    self.skip = True
                elif tag == 'br':
                    self.text.append('\n')
                elif tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    self.text.append('\n\n')

            def handle_endtag(self, tag):
                if tag in ['script', 'style', 'meta', 'link']:
                    self.skip = False

            def handle_data(self, data):
                if not self.skip:
                    self.text.append(data)

        parser = HTMLToText()
        parser.feed(html_content)
        text = ''.join(parser.text)

        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        header = f"# Document from {url}\n\n---\n\n"
        return header + text.strip()


def download_and_process(url: str, target_folder: Path, custom_name: str = None) -> bool:
    """
    Download URL and process based on content type.

    Args:
        url: URL to download
        target_folder: Folder to save to (e.g., reference_docs/yield/)
        custom_name: Optional custom filename

    Returns:
        True if successful
    """
    try:
        # Download content
        print(f"  Fetching: {url}")
        response = requests.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').lower()

        # Determine if HTML or PDF
        is_html = 'html' in content_type or url.lower().endswith('.html')
        is_pdf = 'pdf' in content_type or url.lower().endswith('.pdf')

        # Determine filename
        if custom_name:
            filename = custom_name
        else:
            filename = guess_filename_from_url(url, content_type)

        # Handle HTML conversion
        if is_html:
            print(f"  Converting HTML to markdown...")
            markdown_content = html_to_markdown(response.text, url)

            # Change extension to .md
            if not filename.endswith('.md'):
                filename = filename.rsplit('.', 1)[0] + '.md'

            output_path = target_folder / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown_content, encoding='utf-8')

            print(f"  ✓ Saved as markdown: {output_path}")
            return True

        # Handle PDF (and other binary files)
        else:
            if not filename.endswith('.pdf'):
                filename += '.pdf'

            output_path = target_folder / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)

            print(f"  ✓ Saved as PDF: {output_path}")
            return True

    except Exception as e:
        print(f"  ✗ Error processing {url}: {e}")
        return False


def parse_yaml_file(filepath: Path) -> Dict[str, List[Tuple[str, str]]]:
    """
    Parse YAML file with document URLs.

    Returns:
        Dict mapping folder names to list of (url, custom_name) tuples
    """
    try:
        import yaml
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        result = {}
        for folder, items in data.items():
            if not isinstance(items, list):
                continue

            docs = []
            for item in items:
                if isinstance(item, str):
                    # Simple string format: just URL
                    docs.append((item, None))
                elif isinstance(item, dict):
                    # Dict format: {url: ..., name: ...}
                    url = item.get('url')
                    name = item.get('name')
                    if url:
                        docs.append((url, name))

            if docs:
                result[folder] = docs

        return result

    except ImportError:
        print("ERROR: PyYAML not installed. Install with: pip install pyyaml")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR parsing YAML file: {e}")
        sys.exit(1)


def parse_simple_file(filepath: Path) -> Dict[str, List[Tuple[str, str]]]:
    """
    Parse simple text file with format:
        folder: URL
        folder: URL [custom_name.pdf]

    Returns:
        Dict mapping folder names to list of (url, custom_name) tuples
    """
    result = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Parse: folder: URL [optional_name]
            if ':' not in line:
                print(f"Warning: Line {line_num} invalid format (no colon): {line}")
                continue

            folder, rest = line.split(':', 1)
            folder = folder.strip()
            rest = rest.strip()

            # Check for custom name in brackets
            custom_name = None
            if '[' in rest and ']' in rest:
                url, name_part = rest.split('[', 1)
                url = url.strip()
                custom_name = name_part.split(']')[0].strip()
            else:
                url = rest

            if folder not in result:
                result[folder] = []

            result[folder].append((url, custom_name))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Download public PDFs and HTML for ATLASsemi RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example input file (YAML format):

    methodologies:
      - url: https://example.com/8d-handbook.pdf
        name: 8d_handbook.pdf
      - url: https://example.com/dmaic.html
        name: dmaic_guide.md

    yield:
      - https://example.com/spc-manual.pdf

Example input file (simple text format):

    methodologies: https://example.com/8d-handbook.pdf
    methodologies: https://example.com/dmaic.html [dmaic_guide.md]
    yield: https://example.com/spc-manual.pdf
    operations: https://example.com/factory-physics.pdf [factory_physics.pdf]

Supported folders: methodologies, yield, operations, organizational, support
        """
    )

    parser.add_argument(
        'input_file',
        type=Path,
        help='Input file with URLs (YAML or text format)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('reference_docs'),
        help='Output directory (default: reference_docs/)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be downloaded without actually downloading'
    )

    args = parser.parse_args()

    # Check input file exists
    if not args.input_file.exists():
        print(f"ERROR: Input file not found: {args.input_file}")
        sys.exit(1)

    # Parse input file
    print(f"Reading: {args.input_file}")

    if args.input_file.suffix in ['.yaml', '.yml']:
        docs = parse_yaml_file(args.input_file)
    else:
        docs = parse_simple_file(args.input_file)

    if not docs:
        print("ERROR: No documents found in input file")
        sys.exit(1)

    # Show summary
    total_docs = sum(len(urls) for urls in docs.values())
    print(f"\nFound {total_docs} documents across {len(docs)} folders\n")

    for folder, urls in docs.items():
        print(f"  {folder}/: {len(urls)} documents")

    if args.dry_run:
        print("\n--- DRY RUN MODE ---\n")

    print("\n" + "="*60 + "\n")

    # Download documents
    success_count = 0
    fail_count = 0

    for folder, urls in docs.items():
        target_folder = args.output_dir / folder

        print(f"Processing folder: {folder}/")
        print(f"Target: {target_folder}/\n")

        for url, custom_name in urls:
            if args.dry_run:
                print(f"  Would download: {url}")
                if custom_name:
                    print(f"    Save as: {custom_name}")
                success_count += 1
            else:
                if download_and_process(url, target_folder, custom_name):
                    success_count += 1
                else:
                    fail_count += 1

            print()

    # Summary
    print("="*60)
    print(f"\nSummary:")
    print(f"  ✓ Successful: {success_count}")
    print(f"  ✗ Failed: {fail_count}")

    if not args.dry_run and success_count > 0:
        print(f"\nDocuments saved to: {args.output_dir}/")
        print(f"\nNext step: Index documents with:")
        print(f"  python -m atlassemi.knowledge.indexer --source-dir {args.output_dir}/")


if __name__ == "__main__":
    main()
