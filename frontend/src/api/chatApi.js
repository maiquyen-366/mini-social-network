// Tầng API: các request conversation và lịch sử tin nhắn.
import axiosClient from "./axiosClient";

export const getConversationsRequest = () => axiosClient.get("/chat/conversations/");
export const createConversationRequest = (username) => axiosClient.post("/chat/conversations/", { username });
export const getMessagesRequest = (id) => axiosClient.get(`/chat/conversations/${id}/messages/`);
