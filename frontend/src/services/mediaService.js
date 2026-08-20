// Tầng service frontend: chuẩn hóa URL media từ backend để ảnh luôn hiển thị đúng.
import { BACKEND_ORIGIN } from "../config/environment";

export function resolveMediaUrl(url) {
  if (!url) return "";
  if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("blob:") || url.startsWith("data:")) return url;
  return `${BACKEND_ORIGIN}${url.startsWith("/") ? url : `/${url}`}`;
}
