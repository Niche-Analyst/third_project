// components/layout/Header.tsx
export function Header() {
  return (
    <header className="border-b bg-background">
      <div className="container flex h-14 items-center justify-between">
        <div className="font-bold">ORB AI</div>
        <nav className="text-sm text-muted-foreground">IPTV · PPL · Analytics</nav>
      </div>
    </header>
  );
}


