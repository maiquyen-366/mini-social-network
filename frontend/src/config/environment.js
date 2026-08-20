// Tầng cấu hình frontend: đọc và chuẩn hóa các URL theo từng môi trường chạy.
function trimTrailingSlash(value) {
  return value.replace(/\/+$/, "");
}

function normalizeWebSocketUrl(value) {
  const normalized = trimTrailingSlash(value);
  if (normalized.startsWith("https://")) return normalized.replace("https://", "wss://");
  if (normalized.startsWith("http://")) return normalized.replace("http://", "ws://");
  return normalized;
}

export const API_BASE_URL = trimTrailingSlash(
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
);

export const WS_BASE_URL = normalizeWebSocketUrl(
  import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000",
);

export const BACKEND_ORIGIN = trimTrailingSlash(
  import.meta.env.VITE_BACKEND_ORIGIN || "http://localhost:8000",
);
