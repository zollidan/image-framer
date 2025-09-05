/**
 * The main entry point for the React application.
 *
 * This file renders the root component of the application, wrapping it with
 * the `ThemeProvider` to enable light and dark modes, and `StrictMode` for
 * development-time checks.
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ThemeProvider } from "@/components/theme-provider.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>
);
