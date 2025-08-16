export const Footer = () => {
  const essentialLinks = [
    { name: "Privacy Policy", href: "#" },
    { name: "Terms of Service", href: "#" },
    { name: "Help", href: "#" },
  ];

  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-background border-t border-border">
      <div className="container mx-auto flex items-center justify-between py-3">
        <div className="font-mono text-sm text-muted-foreground font-medium">
          v1.2.0
        </div>
        <nav>
          <ul className="flex items-center gap-6">
            {essentialLinks.map((item) => (
              <li key={item.name}>
                <a
                  href={item.href}
                  className="text-sm text-muted-foreground transition-opacity hover:opacity-75"
                >
                  {item.name}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </footer>
  );
};
