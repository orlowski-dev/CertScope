#!/usr/bin/env python3

from pathlib import Path
import xml.etree.ElementTree as ET

PROJECT_DIR = Path(__file__).resolve().parent.parent / "CertScope"
RESOURCES_DIR = PROJECT_DIR / "Resources"

GRESOURCE_FILE = RESOURCES_DIR / "io.github.orlowski_dev.CertScope.gresource.xml"

RESOURCE_TYPES = {
    "icons": {
        "extension": "*.svg",
        "preprocess": "xml-stripblanks",
    },
    "ui": {
        "extension": "*.ui",
        "preprocess": "xml-stripblanks",
    },
}


def main() -> None:
    tree = ET.parse(GRESOURCE_FILE)
    root = tree.getroot()

    gresource = root.find("gresource")

    if gresource is None:
        raise RuntimeError("Nie znaleziono elementu <gresource>")

    existing_files = {
        element.text
        for element in gresource.findall("file")
        if element.text is not None
    }

    for directory, config in RESOURCE_TYPES.items():
        resource_dir = RESOURCES_DIR / directory

        for path in sorted(resource_dir.rglob(config["extension"])):
            resource_path = path.relative_to(RESOURCES_DIR).as_posix()

            if resource_path in existing_files:
                continue

            attributes = {}

            if config["preprocess"]:
                attributes["preprocess"] = config["preprocess"]

            element = ET.SubElement(
                gresource,
                "file",
                attrib=attributes,
            )
            element.text = resource_path

            existing_files.add(resource_path)
            print(f"Dodano: {resource_path}")

    ET.indent(tree, space="  ")
    tree.write(
        GRESOURCE_FILE,
        encoding="utf-8",
        xml_declaration=True,
    )


if __name__ == "__main__":
    main()