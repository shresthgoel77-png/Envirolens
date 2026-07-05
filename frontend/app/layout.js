import "./globals.css";

export const metadata = {
  title: "Envirolens",
  description: "Real-time Environmental Monitoring",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground">{children}</body>
    </html>
  );
}