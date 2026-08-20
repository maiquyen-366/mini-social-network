// Tầng service frontend: kiểm tra file ảnh trước khi tạo FormData.
export const MAX_IMAGE_SIZE = 5 * 1024 * 1024;
export const IMAGE_ACCEPT = "image/jpeg,image/png,image/webp,image/gif";
const allowedTypes = new Set(["image/jpeg", "image/png", "image/webp", "image/gif"]);
const allowedExtensions = new Set(["jpg", "jpeg", "png", "webp", "gif"]);

export function validateImageFile(file) {
  if (!file) return "";
  const extension = file.name.split(".").pop()?.toLowerCase();
  if (!allowedTypes.has(file.type) || !allowedExtensions.has(extension)) return "Chỉ chấp nhận JPG, JPEG, PNG, WEBP hoặc GIF.";
  if (file.size > MAX_IMAGE_SIZE) return "Ảnh không được lớn hơn 5 MB.";
  return "";
}
