// Tầng page: màn hình đăng nhập.
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const { signIn } = useAuth(); const navigate = useNavigate(); const [form, setForm] = useState({ username: "", password: "" }); const [error, setError] = useState(""); const [loading, setLoading] = useState(false);
  const submit = async (event) => { event.preventDefault(); setError(""); setLoading(true); try { await signIn(form); navigate("/"); } catch (err) { setError(err.response?.data?.message || "Đăng nhập thất bại"); } finally { setLoading(false); } };
  return <main className="auth-page"><div className="auth-brand"><span className="brand-mark">M</span><span>Mini Social</span><p>Một góc nhỏ để kết nối và chia sẻ.</p></div><form className="card form auth-form" onSubmit={submit}><span className="eyebrow">CHÀO MỪNG TRỞ LẠI</span><h1>Đăng nhập</h1><p className="form-subtitle">Đăng nhập để xem những điều mới nhất.</p>{error && <p className="form-error">{error}</p>}<label>Username<input required autoComplete="username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></label><label>Mật khẩu<input required autoComplete="current-password" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label><button className="primary full-button" disabled={loading}>{loading ? "Đang đăng nhập..." : "Đăng nhập"}</button><p className="auth-switch">Chưa có tài khoản? <Link to="/register">Đăng ký ngay</Link></p></form></main>;
}
