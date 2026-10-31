namespace CertScope.Views;

[GObject.Subclass<Adw.ApplicationWindow>(qualifiedName: "MainWindow")]
[Gtk.Template<Gtk.GResource>($"{Shared.ResourcesPrefix}/ui/main-window.ui")]
public partial class MainWindow
{
    partial void Initialize() { }
}
