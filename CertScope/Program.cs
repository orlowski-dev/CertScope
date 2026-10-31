// CertScope
// Copyright (C) 2026-2027 Patryk Orłowski <orlowski.patryk.dev@proton.me>
// SPDX-License-Identifier: GPL-3.0-or-later

using CertScope;
using CertScope.Localization;
using CertScope.Views;

// Initialize native bindings
Gio.Module.Initialize();
GLib.Module.Initialize();
Gtk.Module.Initialize();
Adw.Module.Initialize();

// Initialize translations
Gettext.Initialize();

var resourcePath = Path.Combine(AppContext.BaseDirectory, Shared.ResourcesFileName);

using var resources = Gio.Resource.Load(resourcePath);
resources.Register();

// Register custom GObject subclasses
GirCore.Integration.Initialize();

var application = Adw.Application.New(Shared.ApplicationId, Gio.ApplicationFlags.FlagsNone);

application.OnActivate += (sender, args) =>
{
    var app = (Adw.Application)sender;
    var window = MainWindow.NewWithProperties([]);
    window.SetApplication(app);
    window.Present();
};

return application.RunWithSynchronizationContext(null);
