// Tầng component: gửi hoặc chấp nhận lời mời ngay cạnh tác giả bài viết.
import { useEffect, useState } from "react";
import { acceptFriendRequest, sendFriendRequest } from "../services/friendService";

const labels = {
  none: "+ Kết bạn",
  request_sent: "Đã gửi",
  request_received: "Chấp nhận",
  friends: "Bạn bè",
};

export default function FriendButton({ userId, initialState = "none", requestId = null }) {
  const [state, setState] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setState(initialState);
    setError("");
  }, [initialState, requestId]);

  if (state === "self") return null;

  const act = async () => {
    if (loading || state === "friends" || state === "request_sent") return;
    setLoading(true);
    setError("");
    try {
      const friendship = state === "request_received" && requestId
        ? await acceptFriendRequest(requestId)
        : await sendFriendRequest(userId);
      setState(friendship.status === "accepted" ? "friends" : "request_sent");
      window.dispatchEvent(new Event("friendships.changed"));
    } catch (requestError) {
      setError(requestError.response?.data?.message || "Không thể kết bạn.");
    } finally {
      setLoading(false);
    }
  };

  const disabled = loading || state === "friends" || state === "request_sent";
  return (
    <span className="friend-action-wrap">
      <button
        type="button"
        className={`friend-action friend-action-${state}`}
        onClick={act}
        disabled={disabled}
        title={error || labels[state]}
      >
        {loading ? "Đang xử lý..." : labels[state]}
      </button>
      {error && <small className="friend-action-error">{error}</small>}
    </span>
  );
}
