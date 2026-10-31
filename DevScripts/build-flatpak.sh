#!/usr/bin/bash

# Install required tools (Fedora)
sudo dnf install flatpak flatpak-builder

# Add Flathub repository for the current user
flatpak remote-add --user --if-not-exists \
  flathub https://flathub.org/repo/flathub.flatpakrepo

# Install GNOME SDK
flatpak install --user flathub org.gnome.Sdk//50

# Publish the application
dotnet publish CertScope/CertScope.csproj \
  -c Release \
  -r linux-x64 \
  --self-contained true

# Build and install Flatpak locally
flatpak-builder \
  --user \
  --force-clean \
  --install-deps-from=flathub \
  --repo=.flatpak-repo \
  --install \
  .flatpak-build \
  CertScope/Packaging/io.github.orlowski_dev.CertScope.yml

# Run the installed application
echo "To run application type: flatpak run io.github.orlowski_dev.CertScope"