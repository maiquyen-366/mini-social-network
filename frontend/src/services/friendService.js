// Tầng service frontend: map dữ liệu kết bạn cho UI.
import {
  acceptFriendRequestRequest,
  deleteFriendRequestRequest,
  getFriendsRequest,
  sendFriendRequestRequest,
} from "../api/friendApi";

export const listFriends = async () => (await getFriendsRequest()).data.data;
export const sendFriendRequest = async (userId) => (await sendFriendRequestRequest(userId)).data.data;
export const acceptFriendRequest = async (requestId) => (await acceptFriendRequestRequest(requestId)).data.data;
export const deleteFriendRequest = (requestId) => deleteFriendRequestRequest(requestId);
