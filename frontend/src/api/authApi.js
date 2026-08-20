// Tầng API: các request xác thực và hồ sơ.
import axiosClient from "./axiosClient";

export const loginRequest = (payload) => axiosClient.post("/accounts/login/", payload);
export const registerRequest = (payload) => axiosClient.post("/accounts/register/", payload);
export const refreshRequest = (refresh) => axiosClient.post("/accounts/refresh/", { refresh });
export const getMeRequest = () => axiosClient.get("/accounts/me/");
export const updateMeRequest = (payload) => axiosClient.patch("/accounts/me/", payload);
