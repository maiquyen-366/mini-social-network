// Tầng service frontend: gọi API posts và trả dữ liệu gọn cho UI.
import { createCommentRequest, createPostRequest, deletePostRequest, getCommentsRequest, getPostRequest, getPostsRequest, toggleLikeRequest } from "../api/postApi";

export const listPosts = async (page) => (await getPostsRequest(page)).data;
export const createPost = async (payload) => {
  const formData = new FormData();
  formData.append("content", payload.content);
  if (payload.image_file) formData.append("image_file", payload.image_file);
  return (await createPostRequest(formData)).data.data;
};
export const getPost = async (id) => (await getPostRequest(id)).data.data;
export const deletePost = (id) => deletePostRequest(id);
export const toggleLike = async (id) => (await toggleLikeRequest(id)).data.data;
export const listComments = async (id) => (await getCommentsRequest(id)).data.data;
export const createComment = async (id, payload) => (await createCommentRequest(id, payload)).data.data;
