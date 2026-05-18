#!/usr/bin/env python3
"""Auto-update sitemap.xml with actual file lastmod dates."""

import os
import xml.etree.ElementTree as ET
from datetime import datetime

DOMAIN = "https://ekomuzej.com"
SITEMAP_FILE = "sitemap.xml"

# Static URLs without corresponding files
STATIC_URLS = {
    "": {"priority": "1.0", "changefreq": "daily"},
    "/jarunALPHA.apk": {"priority": "0.8", "changefreq": "monthly"},
    "/jesiJEA.apk": {"priority": "0.8", "changefreq": "monthly"},
}


def get_file_paths():
    """Get all HTML files under pjat/ directory."""
    file_paths = []
    for root, _, files in os.walk("pjat"):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ".")
                file_paths.append(rel_path)
    return sorted(file_paths)


def get_lastmod(file_path):
    """Get last modified date in ISO format."""
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")


def generate_sitemap():
    """Generate updated sitemap XML."""
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Add static URLs
    for path, attrs in STATIC_URLS.items():
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{DOMAIN}{path}"
        if path == "":
            ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        else:
            # Use file mtime for APK files if they exist
            if os.path.exists(path.lstrip("/")):
                ET.SubElement(url, "lastmod").text = get_lastmod(path.lstrip("/"))
            else:
                ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(url, "changefreq").text = attrs["changefreq"]
        ET.SubElement(url, "priority").text = attrs["priority"]

    # Add pjat/ URLs
    for rel_path in get_file_paths():
        url_path = f"/{rel_path}"
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{DOMAIN}/{rel_path}"
        ET.SubElement(url, "lastmod").text = get_lastmod(rel_path)
        ET.SubElement(url, "changefreq").text = "weekly"
        ET.SubElement(url, "priority").text = "0.7"

    # Pretty print XML
    ET.indent(urlset, space="  ")
    tree = ET.ElementTree(urlset)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"Updated {SITEMAP_FILE} with {len(list(urlset))} URLs")


if __name__ == "__main__":
    generate_sitemap()
