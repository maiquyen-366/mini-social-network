// Tầng API: request danh sách và trạng thái đã đọc của thông báo.
import axiosClient from "./axiosClient";

export const getNotificationsRequest = () => axiosClient.get("/notifications/");
export const markNotificationReadRequest = (id) => axiosClient.post(`/notifications/${id}/read/`);
export const markAllNotificationsReadRequest = () => axiosClient.post("/notifications/read-all/");
