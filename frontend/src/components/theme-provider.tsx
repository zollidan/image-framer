import { createContext, useContext, useEffect, useState } from "react";

/**
 * The available color themes.
 */
type Theme = "dark" | "light" | "system";

/**
 * Props for the ThemeProvider component.
 *
 * @property {React.ReactNode} children - The child elements to render.
 * @property {Theme} [defaultTheme="system"] - The default theme to use.
 * @property {string} [storageKey="vite-ui-theme"] - The key to use for storing the theme in local storage.
 */
type ThemeProviderProps = {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
};

/**
 * The state of the theme provider.
 *
 * @property {Theme} theme - The current theme.
 * @property {(theme: Theme) => void} setTheme - A function to set the theme.
 */
type ThemeProviderState = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
};

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
};

const ThemeProviderContext = createContext<ThemeProviderState>(initialState);

/**
 * A component that provides a theme to its children.
 *
 * It manages the current theme, persists it to local storage, and applies
 * the corresponding class to the root HTML element.
 *
 * @param {ThemeProviderProps} props - The props for the component.
 * @returns {JSX.Element} The rendered ThemeProvider.
 */
export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  );

  useEffect(() => {
    const root = window.document.documentElement;

    root.classList.remove("light", "dark");

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light";

      root.classList.add(systemTheme);
      return;
    }

    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme);
      setTheme(theme);
    },
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

/**
 * A hook to access the current theme and a function to set it.
 *
 * @throws {Error} If used outside of a ThemeProvider.
 * @returns {ThemeProviderState} The theme state.
 */
export const useTheme = () => {
  const context = useContext(ThemeProviderContext);

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider");

  return context;
};
