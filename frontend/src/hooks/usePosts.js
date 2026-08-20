// Tầng hook: state feed và các thao tác bài viết.
import { useCallback, useEffect, useState } from "react";
import { createPost, deletePost, listPosts, toggleLike } from "../services/postService";

export const usePosts = () => {
  const [posts, setPosts] = useState([]);
  const [pagination, setPagination] = useState({ count: 0, next: null });
  const [page, setPage] = useState(1);
  const load = useCallback(async (pageNumber = 1, append = false) => {
    const result = await listPosts(pageNumber);
    setPosts((items) => append ? [...items, ...result.data] : result.data);
    setPagination(result.pagination);
    setPage(pageNumber);
  }, []);
  useEffect(() => { load(); }, [load]);
  const addPost = async (payload) => { await createPost(payload); await load(); };
  const removePost = async (id) => { await deletePost(id); setPosts((items) => items.filter((item) => item.id !== id)); };
  const likePost = async (id) => {
    const result = await toggleLike(id);
    setPosts((items) => items.map((item) => (
      item.id === id
        ? { ...item, is_liked: result.is_liked, likes_count: result.likes_count }
        : item
    )));
  };
  const loadMore = () => pagination.next && load(page + 1, true);
  return { posts, pagination, load, loadMore, addPost, removePost, likePost };
};
