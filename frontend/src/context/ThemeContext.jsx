// Tầng context: quản lý lựa chọn light, dark hoặc theme hệ thống.
import { createContext, useEffect, useMemo, useState } from "react";

const STORAGE_KEY = "mini-social-theme";

function getSystemTheme() {
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function getInitialPreference() {
  const savedTheme = localStorage.getItem(STORAGE_KEY);
  return savedTheme === "light" || savedTheme === "dark" ? savedTheme : "system";
}

export const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
  const [preference, setPreference] = useState(getInitialPreference);
  const [systemTheme, setSystemTheme] = useState(getSystemTheme);
  const theme = preference === "system" ? systemTheme : preference;

  useEffect(() => {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const updateSystemTheme = (event) => setSystemTheme(event.matches ? "dark" : "light");
    media.addEventListener?.("change", updateSystemTheme);
    return () => media.removeEventListener?.("change", updateSystemTheme);
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    if (preference === "system") localStorage.removeItem(STORAGE_KEY);
    else localStorage.setItem(STORAGE_KEY, preference);
  }, [preference, theme]);

  const value = useMemo(() => ({
    theme,
    preference,
    toggleTheme: () => setPreference(theme === "dark" ? "light" : "dark"),
  }), [preference, theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
