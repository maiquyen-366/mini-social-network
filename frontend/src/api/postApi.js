// Tầng API: các request bài viết, like và comment.
import axiosClient from "./axiosClient";

export const getPostsRequest = (page = 1) => axiosClient.get(`/posts/?page=${page}`);
export const createPostRequest = (payload) => axiosClient.post("/posts/", payload);
export const getPostRequest = (id) => axiosClient.get(`/posts/${id}/`);
export const deletePostRequest = (id) => axiosClient.delete(`/posts/${id}/`);
export const toggleLikeRequest = (id) => axiosClient.post(`/posts/${id}/like/`);
export const getCommentsRequest = (id) => axiosClient.get(`/posts/${id}/comments/`);
export const createCommentRequest = (id, payload) => axiosClient.post(`/posts/${id}/comments/`, payload);
