// Tầng root frontend: lắp ThemeProvider, AuthProvider, Navbar và router.
import { BrowserRouter } from "react-router-dom";
import Navbar from "./components/Navbar";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import { useAuth } from "./hooks/useAuth";
import AppRouter from "./routes/AppRouter";

function Layout() {
  const { user } = useAuth();
  return <>{user && <Navbar />}<AppRouter /></>;
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AuthProvider>
          <Layout />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}
