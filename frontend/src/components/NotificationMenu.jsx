// Tầng component: chuông, badge và danh sách thông báo trên navbar.
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useNotifications } from "../hooks/useNotifications";
import { acceptFriendRequest, deleteFriendRequest } from "../services/friendService";
import Avatar from "./Avatar";
import { BellIcon } from "./icons/NavIcons";

function formatTime(value) {
  return new Date(value).toLocaleString("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function NotificationMenu() {
  const navigate = useNavigate();
  const menuRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [actionId, setActionId] = useState(null);
  const [error, setError] = useState("");
  const { items, unreadCount, loading, refresh, readOne, readAll } = useNotifications();

  useEffect(() => {
    const closeWhenOutside = (event) => {
      if (!menuRef.current?.contains(event.target)) setOpen(false);
    };
    document.addEventListener("mousedown", closeWhenOutside);
    return () => document.removeEventListener("mousedown", closeWhenOutside);
  }, []);

  const openNotification = async (notification) => {
    if (!notification.is_read) await readOne(notification.id);
    if (notification.post_id) {
      setOpen(false);
      navigate(`/posts/${notification.post_id}`);
    }
  };

  const handleFriendRequest = async (notification, accept) => {
    setActionId(notification.id);
    setError("");
    try {
      if (accept) await acceptFriendRequest(notification.friend_request_id);
      else await deleteFriendRequest(notification.friend_request_id);
      if (!notification.is_read) await readOne(notification.id).catch(() => {});
      await refresh();
      window.dispatchEvent(new Event("friendships.changed"));
    } catch (requestError) {
      setError(requestError.response?.data?.message || "Không thể xử lý lời mời.");
    } finally {
      setActionId(null);
    }
  };

  return (
    <div className="notification-menu" ref={menuRef}>
      <button
        type="button"
        className={`nav-item nav-action notification-trigger ${open ? "active" : ""}`}
        onClick={() => setOpen((current) => !current)}
        title="Thông báo"
        aria-label={`Thông báo${unreadCount ? `, ${unreadCount} chưa đọc` : ""}`}
        aria-expanded={open}
      >
        <BellIcon />
        <span className="nav-label">Thông báo</span>
        {unreadCount > 0 && <span className="notification-badge">{unreadCount > 99 ? "99+" : unreadCount}</span>}
      </button>

      {open && (
        <section className="notification-panel" aria-label="Danh sách thông báo">
          <header>
            <div>
              <strong>Thông báo</strong>
              <small>{unreadCount} chưa đọc</small>
            </div>
            {unreadCount > 0 && <button type="button" onClick={() => readAll().catch(() => {})}>Đọc tất cả</button>}
          </header>

          {error && <p className="notification-error">{error}</p>}
          <div className="notification-list">
            {loading ? <div className="empty-inline">Đang tải...</div> : items.length ? items.map((notification) => {
              const pendingRequest = notification.notification_type === "friend_request"
                && notification.friend_request_status === "pending";
              return (
                <article
                  className={`notification-item ${notification.is_read ? "" : "unread"}`}
                  key={notification.id}
                >
                  <button type="button" className="notification-content" onClick={() => openNotification(notification)}>
                    <Avatar username={notification.actor_username} url={notification.actor_avatar_url} size="small" />
                    <span>
                      <span>{notification.message}</span>
                      <time>{formatTime(notification.created_at)}</time>
                    </span>
                  </button>
                  {pendingRequest && (
                    <div className="notification-actions">
                      <button
                        type="button"
                        className="primary"
                        disabled={actionId === notification.id}
                        onClick={() => handleFriendRequest(notification, true)}
                      >
                        Chấp nhận
                      </button>
                      <button
                        type="button"
                        disabled={actionId === notification.id}
                        onClick={() => handleFriendRequest(notification, false)}
                      >
                        Từ chối
                      </button>
                    </div>
                  )}
                </article>
              );
            }) : <div className="empty-inline">Chưa có thông báo nào.</div>}
          </div>
        </section>
      )}
    </div>
  );
}
