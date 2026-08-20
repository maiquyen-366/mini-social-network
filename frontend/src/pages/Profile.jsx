// Tầng page: xem và cập nhật hồ sơ của người dùng hiện tại.
import { useEffect, useState } from "react";
import Avatar from "../components/Avatar";
import { useAuth } from "../hooks/useAuth";
import { IMAGE_ACCEPT, validateImageFile } from "../services/fileValidation";

export default function Profile() {
  const { user, editProfile } = useAuth();
  const [form, setForm] = useState({ email: "", bio: "" });
  const [avatarFile, setAvatarFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [removeAvatar, setRemoveAvatar] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user) setForm({ email: user.email || "", bio: user.bio || "" });
  }, [user]);

  const chooseAvatar = (event) => {
    const file = event.target.files?.[0];
    const validationError = validateImageFile(file);
    if (validationError) {
      setError(validationError);
      setAvatarFile(null);
      setPreview("");
      return;
    }

    setError("");
    setRemoveAvatar(false);
    setAvatarFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const clearAvatar = () => {
    setAvatarFile(null);
    setPreview("");
  };

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setSaved(false);
    setError("");

    try {
      await editProfile({ ...form, avatar_file: avatarFile, remove_avatar: removeAvatar });
      clearAvatar();
      setRemoveAvatar(false);
      setSaved(true);
    } catch (submitError) {
      setError(submitError.response?.data?.message || "Không thể cập nhật hồ sơ.");
    } finally {
      setSaving(false);
    }
  };

  const displayedAvatar = removeAvatar ? "" : (preview || user?.avatar_url);

  return (
    <main className="container narrow profile-page">
      <section className="profile-cover">
        <div className="profile-identity">
          <div className="profile-avatar">
            {preview && !removeAvatar ? (
              <img src={preview} alt="Xem trước avatar" />
            ) : (
              <Avatar username={user?.username} url={displayedAvatar} size="large" />
            )}
          </div>
          <div className="profile-identity-copy">
            <h1>@{user?.username}</h1>
            <p>Hồ sơ cá nhân</p>
          </div>
        </div>
      </section>

      <form className="card form profile-form-card" onSubmit={submit}>
        <div className="section-heading">
          <div>
            <h2>Thông tin cá nhân</h2>
            <p>Cập nhật những gì mọi người nhìn thấy về bạn.</p>
          </div>
        </div>

        <label>
          Email
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
          />
        </label>

        <label>
          Giới thiệu
          <textarea
            value={form.bio}
            maxLength="500"
            onChange={(event) => setForm({ ...form, bio: event.target.value })}
          />
        </label>

        <div className="avatar-upload-row">
          <Avatar username={user?.username} url={displayedAvatar} size="large" />
          <div className="avatar-upload-controls">
            <label className="upload-button">
              Chọn ảnh đại diện
              <input type="file" accept={IMAGE_ACCEPT} onChange={chooseAvatar} />
            </label>
            {avatarFile && (
              <button type="button" className="text-button" onClick={clearAvatar}>
                Bỏ ảnh đã chọn
              </button>
            )}
            {user?.avatar_url && !avatarFile && (
              <button
                type="button"
                className="text-button"
                onClick={() => {
                  setRemoveAvatar(true);
                  setPreview("");
                }}
              >
                Xóa ảnh hiện tại
              </button>
            )}
            <small>JPG, PNG, WEBP hoặc GIF · tối đa 5 MB</small>
          </div>
        </div>

        {error && <p className="form-error">{error}</p>}
        {saved && <p className="success">Đã cập nhật hồ sơ.</p>}
        <button className="primary" disabled={saving}>
          {saving ? "Đang lưu..." : "Lưu thay đổi"}
        </button>
      </form>
    </main>
  );
}
