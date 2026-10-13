// Tầng service frontend: gọi API và tạo WebSocket thông báo.
import {
  getNotificationsRequest,
  markAllNotificationsReadRequest,
  markNotificationReadRequest,
} from "../api/notificationApi";
import { WS_BASE_URL } from "../config/environment";

export const listNotifications = async () => (await getNotificationsRequest()).data.data;
export const markNotificationRead = async (id) => (await markNotificationReadRequest(id)).data.data;
export const markAllNotificationsRead = () => markAllNotificationsReadRequest();

export const createNotificationSocket = () => {
  const token = localStorage.getItem("access_token");
  return new WebSocket(`${WS_BASE_URL}/ws/notifications/?token=${encodeURIComponent(token || "")}`);
};
