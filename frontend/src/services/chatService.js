// Tầng service frontend: gọi API chat và tạo WebSocket room.
import { createConversationRequest, getConversationsRequest, getMessagesRequest } from "../api/chatApi";
import { WS_BASE_URL } from "../config/environment";

export const listConversations = async () => (await getConversationsRequest()).data.data;
export const createConversation = async (username) => (await createConversationRequest(username)).data.data;
export const listMessages = async (id) => (await getMessagesRequest(id)).data.data;
export const createChatSocket = (conversationId) => {
  const token = localStorage.getItem("access_token");
  return new WebSocket(`${WS_BASE_URL}/ws/chat/${conversationId}/?token=${encodeURIComponent(token || "")}`);
};

export const createChatSidebarSocket = () => {
  const token = localStorage.getItem("access_token");
  return new WebSocket(`${WS_BASE_URL}/ws/chat/sidebar/?token=${encodeURIComponent(token || "")}`);
};
