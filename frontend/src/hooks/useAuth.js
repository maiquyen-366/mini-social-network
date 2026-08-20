// Tầng hook: truy cập AuthContext thuận tiện trong component.
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export const useAuth = () => useContext(AuthContext);
