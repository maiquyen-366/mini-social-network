// Tầng page: danh sách phòng, tạo phòng và chat realtime qua WebSocket.
import { useEffect, useRef, useState } from "react";
import Avatar from "../components/Avatar";
import EmojiPicker from "../components/EmojiPicker";
import { SendIcon } from "../components/icons/NavIcons";
import { useAuth } from "../hooks/useAuth";
import { useChat } from "../hooks/useChat";
import { createConversation } from "../services/chatService";
import { listFriends } from "../services/friendService";

function otherParticipant(conversation, userId) {
  return conversation?.participants?.find((participant) => participant.id !== userId)
    || conversation?.participants?.[0];
}

function formatSidebarTime(value) {
  if (!value) return "";
  const date = new Date(value);
  const today = new Date();
  if (date.toDateString() === today.toDateString()) {
    return date.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
  }
  return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit" });
}

export default function Chat() {
  const { user } = useAuth();
  const {
    conversations,
    active,
    messages,
    connected,
    upsertConversation,
    openConversation,
    deactivateRoom,
    sendMessage,
  } = useChat();
  const [friends, setFriends] = useState([]);
  const [openingFriendId, setOpeningFriendId] = useState(null);
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [roomOpen, setRoomOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const messageInputRef = useRef(null);

  const startChatWithFriend = async (friend) => {
    const existingConversation = conversations.find((conversation) => (
      conversation.participants?.some((participant) => participant.id === friend.id)
    ));
    if (existingConversation) {
      openConversation(existingConversation);
      setRoomOpen(true);
      return;
    }

    setOpeningFriendId(friend.id);
    try {
      const conversation = await createConversation(friend.username);
      upsertConversation(conversation);
      openConversation(conversation);
      setRoomOpen(true);
      setError("");
    } catch (requestError) {
      setError(requestError.response?.data?.message || "Không thể mở cuộc trò chuyện.");
    } finally {
      setOpeningFriendId(null);
    }
  };

  const sendCurrentMessage = () => {
    if (!content.trim() || !connected) return;
    if (sendMessage(content)) setContent("");
  };

  const submit = (event) => {
    event.preventDefault();
    sendCurrentMessage();
  };

  const handleMessageKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
      event.preventDefault();
      sendCurrentMessage();
    }
  };

  const insertEmoji = (emoji) => {
    const input = messageInputRef.current;
    const selectionStart = input?.selectionStart ?? content.length;
    const selectionEnd = input?.selectionEnd ?? content.length;
    const nextContent = `${content.slice(0, selectionStart)}${emoji}${content.slice(selectionEnd)}`;
    if (nextContent.length > 2000) return;

    const nextCursor = selectionStart + emoji.length;
    setContent(nextContent);
    requestAnimationFrame(() => {
      input?.focus();
      input?.setSelectionRange(nextCursor, nextCursor);
    });
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    let activeEffect = true;
    const loadFriends = () => {
      listFriends()
        .then((items) => {
          if (activeEffect) setFriends(items);
        })
        .catch(() => {
          if (activeEffect) setError("Không thể tải danh sách bạn bè.");
        });
    };

    loadFriends();
    window.addEventListener("friendships.changed", loadFriends);
    return () => {
      activeEffect = false;
      window.removeEventListener("friendships.changed", loadFriends);
    };
  }, []);

  const activeOther = otherParticipant(active, user?.id);
  const friendsWithoutConversation = friends.filter((friend) => !conversations.some((conversation) => (
    conversation.participants?.some((participant) => participant.id === friend.id)
  )));

  return (
    <main className={`chat-layout ${roomOpen ? "room-open" : ""}`}>
      <aside className="card chat-sidebar">
        <div className="chat-sidebar-head">
          <div>
            <span className="eyebrow">TIN NHẮN</span>
            <h1>Cuộc trò chuyện</h1>
          </div>
          <span className="count-badge">{conversations.length}</span>
        </div>

        {error && <p className="form-error">{error}</p>}

        <div className="conversation-list">
          {conversations.length ? conversations.map((conversation) => {
            const participant = otherParticipant(conversation, user?.id);
            const isMine = conversation.last_message_sender_id === user?.id;
            const preview = conversation.last_message_content
              ? `${isMine ? "Bạn: " : ""}${conversation.last_message_content}`
              : "Chưa có tin nhắn";
            const hasUnread = conversation.unread_count > 0;
            return (
              <button
                className={`conversation ${active?.id === conversation.id ? "active" : ""} ${hasUnread ? "unread" : ""}`}
                onClick={() => {
                  openConversation(conversation);
                  setRoomOpen(true);
                }}
                key={conversation.id}
              >
                <Avatar username={participant?.username} url={participant?.avatar_url} size="medium" />
                <span className="conversation-details">
                  <span className="conversation-title-row">
                    <strong>{participant?.username || "Cuộc trò chuyện"}</strong>
                    <time dateTime={conversation.last_message_at || undefined}>
                      {formatSidebarTime(conversation.last_message_at)}
                    </time>
                  </span>
                  <span className="conversation-preview-row">
                    <small>{preview}</small>
                    {hasUnread && (
                      <span className="unread-badge" aria-label={`${conversation.unread_count} tin chưa đọc`}>
                        {conversation.unread_count > 99 ? "99+" : conversation.unread_count}
                      </span>
                    )}
                  </span>
                </span>
              </button>
            );
          }) : <div className="empty-inline">Chưa có cuộc trò chuyện nào.</div>}

          <div className="friend-list-heading">
            <span>Bạn bè</span>
            <small>{friends.length}</small>
          </div>
          {friendsWithoutConversation.map((friend) => (
            <button
              type="button"
              className="friend-chat-item"
              key={friend.id}
              disabled={openingFriendId === friend.id}
              onClick={() => startChatWithFriend(friend)}
            >
              <Avatar username={friend.username} url={friend.avatar_url} size="medium" />
              <span>
                <strong>{friend.username}</strong>
                <small>{openingFriendId === friend.id ? "Đang mở..." : "Nhắn tin"}</small>
              </span>
            </button>
          ))}
          {!friends.length && <div className="empty-inline friend-empty">Hãy kết bạn từ Newsfeed để bắt đầu chat.</div>}
        </div>
      </aside>

      <section className="card chat-room">
        {active ? (
          <>
            <div className="chat-room-head">
              <button
                className="back-button"
                onClick={() => {
                  deactivateRoom();
                  setRoomOpen(false);
                }}
                aria-label="Quay lại danh sách cuộc trò chuyện"
              >
                ←
              </button>
              <Avatar username={activeOther?.username} url={activeOther?.avatar_url} />
              <div>
                <h2>{activeOther?.username || "Cuộc trò chuyện"}</h2>
                <span>Trò chuyện riêng tư</span>
              </div>
            </div>

            <div className="messages">
              {messages.length ? messages.map((message) => (
                <div
                  className={`message-row ${message.sender === user?.id ? "mine" : "theirs"}`}
                  key={message.id}
                >
                  <Avatar
                    username={message.sender_username}
                    url={message.sender_avatar_url}
                    size="small"
                  />
                  <div className="message">
                    <span>{message.content}</span>
                    <small>
                      {new Date(message.created_at).toLocaleTimeString("vi-VN", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                      {message.sender === user?.id && ` · ${message.read_at ? "Đã xem" : "Đã gửi"}`}
                    </small>
                  </div>
                </div>
              )) : <div className="empty-inline">Hãy gửi lời chào đầu tiên.</div>}
              <div ref={messagesEndRef} />
            </div>

            <form className="chat-input" onSubmit={submit}>
              <EmojiPicker onSelect={insertEmoji} disabled={!connected} />
              <textarea
                ref={messageInputRef}
                value={content}
                onChange={(event) => setContent(event.target.value)}
                onKeyDown={handleMessageKeyDown}
                placeholder="Nhập tin nhắn..."
                aria-label="Nội dung tin nhắn"
                maxLength="2000"
                rows="1"
              />
              <button
                className="primary chat-send-button"
                disabled={!content.trim() || !connected}
                title={connected ? "Gửi tin nhắn" : "Đang kết nối WebSocket"}
                aria-label="Gửi tin nhắn"
              >
                <SendIcon />
                <span className="send-label">Gửi</span>
              </button>
            </form>
          </>
        ) : (
          <div className="chat-empty">
            <span>✦</span>
            <h2>Chọn một cuộc trò chuyện</h2>
            <p>Tin nhắn của bạn sẽ xuất hiện ở đây.</p>
          </div>
        )}
      </section>
    </main>
  );
}
