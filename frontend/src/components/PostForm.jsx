// Tầng component: form tạo bài đăng, chọn ảnh và chèn emoji Unicode.
import { useRef, useState } from "react";
import { IMAGE_ACCEPT, validateImageFile } from "../services/fileValidation";
import Avatar from "./Avatar";
import EmojiPicker from "./EmojiPicker";

const MAX_CONTENT_LENGTH = 5000;

export default function PostForm({ user, onSubmit }) {
  const [content, setContent] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const textareaRef = useRef(null);

  const chooseImage = (event) => {
    const file = event.target.files?.[0];
    const validationError = validateImageFile(file);
    if (validationError) {
      setError(validationError);
      setImageFile(null);
      setPreview("");
      return;
    }

    setError("");
    setImageFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const clearImage = () => {
    setImageFile(null);
    setPreview("");
    setError("");
  };

  const insertEmoji = (emoji) => {
    const textarea = textareaRef.current;
    const selectionStart = textarea?.selectionStart ?? content.length;
    const selectionEnd = textarea?.selectionEnd ?? content.length;
    const nextContent = `${content.slice(0, selectionStart)}${emoji}${content.slice(selectionEnd)}`;

    if (nextContent.length > MAX_CONTENT_LENGTH) {
      setError(`Nội dung tối đa ${MAX_CONTENT_LENGTH} ký tự.`);
      return;
    }

    const nextCursor = selectionStart + emoji.length;
    setContent(nextContent);
    setError("");
    requestAnimationFrame(() => {
      textarea?.focus();
      textarea?.setSelectionRange(nextCursor, nextCursor);
    });
  };

  const submit = async (event) => {
    event.preventDefault();
    if (!content.trim()) {
      setError("Hãy viết nội dung bài viết.");
      return;
    }

    setSaving(true);
    try {
      await onSubmit({ content, image_file: imageFile });
      setContent("");
      clearImage();
    } catch (submitError) {
      setError(submitError.response?.data?.message || "Không thể đăng bài.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="card composer" onSubmit={submit}>
      <div className="composer-head">
        <Avatar username={user?.username} url={user?.avatar_url} />
        <div>
          <strong>Tạo bài viết</strong>
          <span>Chia sẻ điều gì đó với mọi người</span>
        </div>
      </div>

      <textarea
        ref={textareaRef}
        aria-label="Nội dung bài viết"
        placeholder="Bạn đang nghĩ gì?"
        value={content}
        maxLength={MAX_CONTENT_LENGTH}
        onChange={(event) => setContent(event.target.value)}
      />

      {preview && (
        <div className="image-preview">
          <img src={preview} alt="Xem trước ảnh bài viết" />
          <button type="button" className="remove-image" onClick={clearImage}>Bỏ ảnh</button>
        </div>
      )}

      {error && <p className="form-error">{error}</p>}

      <div className="composer-actions">
        <div className="composer-tools">
          <label className="upload-button">
            <span>＋</span>
            Thêm ảnh
            <input type="file" accept={IMAGE_ACCEPT} onChange={chooseImage} />
          </label>
          <EmojiPicker
            className="composer-emoji-picker"
            onSelect={insertEmoji}
            disabled={saving}
            ariaLabel="Chèn emoji"
            title="Chèn emoji vào bài viết"
          />
        </div>
        <button className="primary" type="submit" disabled={saving}>
          {saving ? "Đang đăng..." : "Đăng bài"}
        </button>
      </div>
    </form>
  );
}
