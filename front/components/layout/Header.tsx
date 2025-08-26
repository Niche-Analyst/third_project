// components/layout/Header.tsx
export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center justify-between">
        <div className="font-extrabold tracking-tight">ORB AI</div>
        <nav className="hidden sm:block text-sm text-muted-foreground">
          IPTV · PPL · Analytics
        </nav>
      </div>
    </header>
  );
}
