// Centralized API base and URL helper
// Ensures we don't end up with "undefined" in URLs when env isn't set

const rawBase = (import.meta as any)?.env?.VITE_API_URL as string | undefined;

// Normalize: empty string when not provided, trim trailing slash
export const API_BASE = (rawBase ?? "").replace(/\/+$/, "");

// Join helper: always returns absolute path starting with origin or '/'
export function apiPath(path: string): string {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  // Prefer absolute base if provided, else rely on same-origin relative path
  return API_BASE ? `${API_BASE}${normalized}` : normalized;
}

