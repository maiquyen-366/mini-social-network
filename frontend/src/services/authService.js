// Tầng service frontend: map response xác thực và quản lý token localStorage.
import { getMeRequest, loginRequest, registerRequest, updateMeRequest } from "../api/authApi";

const saveTokens = (data) => {
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  localStorage.setItem("current_user", JSON.stringify(data.user));
  return data.user;
};

export const login = async (payload) => saveTokens((await loginRequest(payload)).data.data);
export const register = async (payload) => saveTokens((await registerRequest(payload)).data.data);
export const getCurrentUser = async () => (await getMeRequest()).data.data;
export const updateProfile = async (payload) => {
  const formData = new FormData();
  if (payload.email !== undefined) formData.append("email", payload.email);
  if (payload.bio !== undefined) formData.append("bio", payload.bio);
  if (payload.avatar_file) formData.append("avatar_file", payload.avatar_file);
  if (payload.remove_avatar) formData.append("remove_avatar", "true");
  const user = (await updateMeRequest(formData)).data.data;
  localStorage.setItem("current_user", JSON.stringify(user));
  return user;
};
export const logout = () => localStorage.clear();
