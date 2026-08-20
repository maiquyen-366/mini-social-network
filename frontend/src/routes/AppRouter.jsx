// Tầng route frontend: bảo vệ các trang cần đăng nhập.
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Chat from "../pages/Chat";
import Feed from "../pages/Feed";
import Login from "../pages/Login";
import PostDetail from "../pages/PostDetail";
import Profile from "../pages/Profile";
import Register from "../pages/Register";

function PrivateRoute({ children }) { const { user, loading } = useAuth(); if (loading) return <p className="page-loading">Đang tải...</p>; return user ? children : <Navigate to="/login" replace />; }

export default function AppRouter() {
  return <Routes><Route path="/login" element={<Login />} /><Route path="/register" element={<Register />} /><Route path="/" element={<PrivateRoute><Feed /></PrivateRoute>} /><Route path="/posts/:id" element={<PrivateRoute><PostDetail /></PrivateRoute>} /><Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} /><Route path="/chat" element={<PrivateRoute><Chat /></PrivateRoute>} /><Route path="*" element={<Navigate to="/" replace />} /></Routes>;
}
