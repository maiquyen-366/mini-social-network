// Tầng hook: cung cấp theme hiện tại cho component.
import { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme phải được dùng bên trong ThemeProvider.");
  return context;
}
