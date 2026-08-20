// Tầng component: avatar có chữ cái mặc định và fallback khi ảnh lỗi.
import { useState } from "react";
import { resolveMediaUrl } from "../services/mediaService";

export default function Avatar({ username = "User", url = "", size = "medium", className = "" }) {
  const [failed, setFailed] = useState(false);
  const initial = username.trim().charAt(0).toUpperCase() || "U";
  const showImage = url && !failed;
  return <span className={`avatar avatar-${size} ${className}`} aria-label={`Avatar của ${username}`}>{showImage ? <img src={resolveMediaUrl(url)} alt="" onError={() => setFailed(true)} /> : initial}</span>;
}
