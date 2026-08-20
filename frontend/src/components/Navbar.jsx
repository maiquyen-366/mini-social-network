// Tầng component: điều hướng chính, đổi theme và đăng xuất.
import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useTheme } from "../hooks/useTheme";
import Avatar from "./Avatar";
import Logo from "./Logo";
import { ChatIcon, HomeIcon, LogoutIcon, MoonIcon, SunIcon } from "./icons/NavIcons";

function navClass({ isActive }) {
  return `nav-item ${isActive ? "active" : ""}`;
}

export default function Navbar() {
  const { user, signOut } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const nextThemeLabel = theme === "dark" ? "Chuyển sang chế độ sáng" : "Chuyển sang chế độ tối";

  return (
    <header className="navbar">
      <Link className="brand" to="/" aria-label="Mini Social - Trang chủ">
        <Logo />
        <span className="brand-text">Mini Social</span>
      </Link>

      <nav className="nav-links" aria-label="Điều hướng chính">
        <NavLink className={navClass} to="/" end title="Feed" aria-label="Feed">
          <HomeIcon />
          <span className="nav-label">Feed</span>
        </NavLink>
        <NavLink className={navClass} to="/chat" title="Chat" aria-label="Chat">
          <ChatIcon />
          <span className="nav-label">Chat</span>
        </NavLink>
        <button
          type="button"
          className="nav-item nav-action"
          onClick={toggleTheme}
          title={nextThemeLabel}
          aria-label={nextThemeLabel}
        >
          {theme === "dark" ? <SunIcon /> : <MoonIcon />}
          <span className="nav-label">{theme === "dark" ? "Sáng" : "Tối"}</span>
        </button>
        <NavLink className={({ isActive }) => `nav-item nav-profile ${isActive ? "active" : ""}`} to="/profile" title="Hồ sơ" aria-label="Hồ sơ">
          <Avatar username={user?.username} url={user?.avatar_url} size="small" />
          <span className="profile-label">{user?.username}</span>
        </NavLink>
        <button
          type="button"
          className="nav-item nav-action nav-logout"
          onClick={signOut}
          title="Đăng xuất"
          aria-label="Đăng xuất"
        >
          <LogoutIcon />
          <span className="nav-label">Đăng xuất</span>
        </button>
      </nav>
    </header>
  );
}
