import argparse
import os
from rich.console import Console
from rich.markdown import Markdown

# Initialize the console
console = Console()

# Set up argument parser
parser = argparse.ArgumentParser(description="Display a TLDR page in the terminal")
parser.add_argument("entry", help="The TLDR page to display (e.g., git, ls)")
args = parser.parse_args()

# Possible OS-specific subdirectories (based on common tldr-pages structure)
os_variants = ["android", "common", "freebsd", "linux", "netbsd", "openbsd", "osx", "sunos", "windows"]

# Base path for tldr-pages
base_path = os.path.expanduser("~/tldr-pages.en")

# Try to find the Markdown file in one of the OS-specific subdirectories
# Download from https://github.com/tldr-pages/tldr/releases/latest
markdown_file = None
for os_variant in os_variants:
    file_path = os.path.join(base_path, os_variant, f"{args.entry}.md")
    if os.path.isfile(file_path):
        markdown_file = file_path
        break

# Check if a file was found
if not markdown_file:
    console.print(f"[red]Error: TLDR page for '{args.entry}' not found in any OS-specific directory under {base_path}[/red]")
    exit(1)

# Read and print the Markdown content
try:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    md = Markdown(markdown_content, code_theme="default", inline_code_lexer="bash", inline_code_theme="default")
    console.print(md)
except Exception as e:
    console.print(f"[red]Error reading file: {e}[/red]")
    exit(1)

"""
tldr() {
    local entry="$1"
    if [ -z "$entry" ]; then
        echo "Error: Please provide a TLDR entry (e.g., tldr git)"
        return 1
    fi
    /home/wangyh/anaconda3/envs/black/bin/python /home/wangyh/tldr-pages.py "$entry"
}
"""
