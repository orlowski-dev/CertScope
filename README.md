# CertScope

## Building

### System requirements

```bash
sudo dnf install \
    git \
    flatpak \
    flatpak-builder \
    dotnet-sdk-10.0 \
    gtk4 \
    libadwaita \
    glib2-devel \
    gettext \
    flatpak \
    flatpak-builder
    blueprint-compiler
```

## Localization

CertScope uses **GNU Gettext** to provide translations. Translation files are stored in the `CertScope/po/` directory.

### Directory structure

```text
CertScope/
├── Localization/
│   └── Gettext.cs
└── po/
    ├── messages.pot    # Translation template
    └── pl.po           # Polish translations
```

- `messages.pot` - Translation template containing the original strings.
- `pl.po` - Polish translations. Additional languages use their corresponding language codes (e.g., `de.po`, `fr.po`).
- `.mo` - Compiled binary translations generated automatically during the build.

### 1. Updating translations

When new translatable strings are added or existing strings are modified, update the translation template.

Extract strings from C# source files using `xgettext`:

```bash
chmod +x ./DevScripts/update-translations.py
./DevScripts/update-translations.py
```

Merge the updated template into existing translations:

```bash
msgmerge --update po/pl.po po/messages.pot
```

After merging, open `po/pl.po` and translate any new or modified entries.

### 2. Adding a new language

Create a translation file from the template:

```bash
msginit \
  --input=po/messages.pot \
  --output-file=po/de.po \
  --locale=de_DE.UTF-8
```

Replace `de_DE.UTF-8` with the desired locale.

### 3. Validating translations

Check translation files for formatting errors:

```bash
msgfmt --check po/pl.po
```

### 4. Building translations

Translations are automatically compiled into `.mo` files during `dotnet build` and `dotnet publish`.

```bash
dotnet build
```

The resulting files are placed in locale-specific directories:

```text
locale/
└── pl/
    └── LC_MESSAGES/
        └── io.github.orlowski_dev.CertScope.mo
```

There is no need to commit generated `.mo` files to the repository.

### 5. Testing a translation

Launch CertScope with a specific locale:

```bash
LANGUAGE=pl_PL:pl LANG=pl_PL.UTF-8 dotnet run --project CertScope
```

To test the default English interface:

```bash
LANGUAGE=en LANG=en_US.UTF-8 dotnet run --project CertScope
```

The requested locale must be available on the system.

### Translation guidelines

- Keep the original meaning of each message.
- Preserve placeholders such as `{0}`, `%s`, and `%d`.
- Do not translate technical identifiers, file paths, or command names unless necessary.
- Use consistent terminology throughout the application.
- Commit `.po` and `.pot` files, but exclude generated `.mo` files.

## Developer Resources

The following resources provide documentation for the frameworks, libraries, and development tools used in CertScope.

| Technology               | Documentation                                                                                                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GirCore**              | [Documentation](https://gircore.github.io/index.html) · [Getting Started](https://gircore.github.io/docs/get-started.html) · [GitHub](https://github.com/gircore/gir.core) |
| **GTK 4**                | [API Reference](https://docs.gtk.org/gtk4/) · [GTK Inspector](https://developer.gnome.org/documentation/tools/inspector.html)                                              |
| **libadwaita**           | [API Reference](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/)                                                                                             |
| **GLib / GObject / GIO** | [GLib](https://docs.gtk.org/glib/) · [GObject](https://docs.gtk.org/gobject/) · [GIO](https://docs.gtk.org/gio/)                                                           |
| **GNOME**                | [Developer Documentation](https://developer.gnome.org/documentation/) · [Human Interface Guidelines](https://developer.gnome.org/hig/)                                     |
| **.NET 10 / C#**         | [.NET Documentation](https://learn.microsoft.com/en-us/dotnet/) · [C# Reference](https://learn.microsoft.com/en-us/dotnet/csharp/)                                         |
| **Dependency Injection** | [Microsoft.Extensions.DependencyInjection](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/)                                                 |
| **GResource**            | [GResource Documentation](https://docs.gtk.org/gio/struct.Resource.html)                                                                                                   |
| **Gettext**              | [GNU Gettext Manual](https://www.gnu.org/software/gettext/manual/)                                                                                                         |
| **Flatpak**              | [Developer Documentation](https://docs.flatpak.org/en/latest/) · [Flatpak Builder](https://docs.flatpak.org/en/latest/flatpak-builder.html)                                |

### Development Tools

- [Cambalache](https://gitlab.gnome.org/jpu/cambalache) - visual editor for GTK user interfaces.
- [GNOME Workbench](https://apps.gnome.org/Workbench/) - interactive environment for experimenting with GTK and libadwaita widgets.
- [GTK Inspector](https://developer.gnome.org/documentation/tools/inspector.html) - runtime inspection and debugging of GTK widgets, properties, and CSS.

## License

CertScope is free software licensed under the GNU General Public License, version 3 or any later version (`GPL-3.0-or-later`).

Copyright (C) 2026–2027 Patryk Orłowski  
Contact: orlowski.patryk.dev@proton.me

You may redistribute and/or modify this software under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This software is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the [LICENSE](LICENSE) file for the full license text.

The copyright and licensing terms of third-party dependencies and assets remain governed by their respective licenses.
