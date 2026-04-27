import "./globals.css";

export const metadata = {
  title: "MomzCare",
  description: "Refined Arabic support replies for Mumzworld.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
