using CertScope;
using CertScope.Localization;

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
    var builder = Gtk.Builder.NewFromResource($"{Shared.ResourcesPrefix}/ui/main-window.ui");

    var content =
        builder.GetObject("mainContent") as Gtk.Widget
        ?? throw new InvalidOperationException("'mainContent' widget not found.");

    var window = Adw.ApplicationWindow.New(app);
    window.SetTitle("MyNetGtkApp");
    window.SetDefaultSize(1000, 700);
    window.SetContent(content);
    window.Present();
};

return application.RunWithSynchronizationContext(null);
