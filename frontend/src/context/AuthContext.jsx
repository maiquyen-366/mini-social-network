// Tầng context: giữ user hiện tại và các hành động xác thực toàn app.
import { createContext, useEffect, useState } from "react";
import { getCurrentUser, login, logout, register, updateProfile } from "../services/authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("current_user") || "null"));
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    if (!localStorage.getItem("access_token")) { setLoading(false); return; }
    getCurrentUser().then(setUser).catch(() => { logout(); setUser(null); }).finally(() => setLoading(false));
  }, []);
  const signIn = async (payload) => setUser(await login(payload));
  const signUp = async (payload) => setUser(await register(payload));
  const signOut = () => { logout(); setUser(null); };
  const editProfile = async (payload) => setUser(await updateProfile(payload));
  return <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut, editProfile }}>{children}</AuthContext.Provider>;
}
