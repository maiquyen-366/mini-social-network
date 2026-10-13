// Tầng hook: giữ danh sách, badge và kết nối thông báo realtime.
import { useCallback, useEffect, useRef, useState } from "react";
import {
  createNotificationSocket,
  listNotifications,
  markAllNotificationsRead,
  markNotificationRead,
} from "../services/notificationService";

export const useNotifications = () => {
  const [items, setItems] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const reconnectTimerRef = useRef(null);

  const refresh = useCallback(async () => {
    try {
      const result = await listNotifications();
      setItems(result.items);
      setUnreadCount(result.unread_count);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh().catch(() => {});
  }, [refresh]);

  useEffect(() => {
    let stopped = false;
    let activeSocket = null;

    const connect = () => {
      if (stopped) return;
      try {
        const socket = createNotificationSocket();
        activeSocket = socket;
        socket.onmessage = (event) => {
          const payload = JSON.parse(event.data);
          if (payload.type === "notifications.changed") refresh().catch(() => {});
        };
        socket.onerror = () => socket.close();
        socket.onclose = (event) => {
          if (!stopped && event.code !== 4001) {
            reconnectTimerRef.current = setTimeout(connect, 2500);
          }
        };
      } catch {
        reconnectTimerRef.current = setTimeout(connect, 2500);
      }
    };

    connect();
    return () => {
      stopped = true;
      clearTimeout(reconnectTimerRef.current);
      activeSocket?.close();
    };
  }, [refresh]);

  const readOne = async (id) => {
    await markNotificationRead(id);
    await refresh();
  };

  const readAll = async () => {
    await markAllNotificationsRead();
    await refresh();
  };

  return { items, unreadCount, loading, refresh, readOne, readAll };
};
