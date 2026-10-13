// Tầng API: request lời mời và danh sách bạn bè.
import axiosClient from "./axiosClient";

export const getFriendsRequest = () => axiosClient.get("/accounts/friends/");
export const sendFriendRequestRequest = (userId) => axiosClient.post("/accounts/friend-requests/", { user_id: userId });
export const acceptFriendRequestRequest = (requestId) => axiosClient.post(`/accounts/friend-requests/${requestId}/accept/`);
export const deleteFriendRequestRequest = (requestId) => axiosClient.delete(`/accounts/friend-requests/${requestId}/`);
