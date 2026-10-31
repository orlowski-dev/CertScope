using System.Runtime.InteropServices;

namespace CertScope.Localization;

public static class Gettext
{
    public const string Domain = "io.github.orlowski_dev.CertScope";

    private const int LcAll = 6; // LC_ALL w glibc (Linux)

    [DllImport("libc.so.6", EntryPoint = "setlocale")]
    private static extern nint SetLocale(
        int category,
        [MarshalAs(UnmanagedType.LPUTF8Str)] string locale
    );

    [DllImport("libc.so.6", EntryPoint = "bindtextdomain")]
    private static extern nint BindTextDomain(
        [MarshalAs(UnmanagedType.LPUTF8Str)] string domain,
        [MarshalAs(UnmanagedType.LPUTF8Str)] string directory
    );

    [DllImport("libc.so.6", EntryPoint = "bind_textdomain_codeset")]
    private static extern nint BindTextDomainCodeset(
        [MarshalAs(UnmanagedType.LPUTF8Str)] string domain,
        [MarshalAs(UnmanagedType.LPUTF8Str)] string codeset
    );

    public static void Initialize()
    {
        var localeDirectory = Path.Combine(AppContext.BaseDirectory, "locale");

        if (SetLocale(LcAll, "") == 0)
            throw new InvalidOperationException("Cannot initialize system locale.");

        if (BindTextDomain(Domain, localeDirectory) == 0)
            throw new InvalidOperationException("Cannot bind Gettext translation domain.");

        if (BindTextDomainCodeset(Domain, "UTF-8") == 0)
            throw new InvalidOperationException("Cannot configure Gettext encoding.");
    }

    public static string Get(string message) => GLib.Functions.Dgettext(Domain, message);

    public static string GetPlural(string singular, string plural, ulong count) =>
        GLib.Functions.Dngettext(Domain, singular, plural, count);
}
