// Tầng page: chi tiết bài đăng và danh sách bình luận.
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createComment, deletePost, getPost, listComments, toggleLike } from "../services/postService";
import PostCard from "../components/PostCard";
import Avatar from "../components/Avatar";

export default function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [content, setContent] = useState("");

  useEffect(() => {
    getPost(id).then(setPost);
    listComments(id).then(setComments);
  }, [id]);

  const submit = async (event) => {
    event.preventDefault();
    if (!content.trim()) return;

    const comment = await createComment(id, { content });
    setComments([...comments, comment]);
    setContent("");
  };

  if (!post) {
    return <main className="container">Đang tải...</main>;
  }

  const like = async () => {
    const result = await toggleLike(post.id);
    setPost((current) => ({ ...current, ...result }));
  };
  const remove = async () => {
    await deletePost(post.id);
    navigate("/");
  };

  return (
    <main className="container detail-page">
      <PostCard
        post={post}
        currentUser={user}
        onLike={like}
        onDelete={remove}
      />

      <section className="card comments-card">
        <header className="comments-header">
          <h2 className="comments-title">Bình luận</h2>
          <p className="comments-count">
            {comments.length} bình luận trong bài viết này
          </p>
        </header>

        <div className="comments-list">
          {comments.length ? comments.map((comment) => (
            <div className="comment" key={comment.id}>
              <Avatar
                username={comment.author_username}
                url={comment.author_avatar_url}
                size="small"
              />
              <div className="comment-body">
                <strong>{comment.author_username}</strong>
                <p>{comment.content}</p>
              </div>
            </div>
          )) : (
            <div className="empty-inline">
              Chưa có bình luận nào. Hãy viết bình luận đầu tiên.
            </div>
          )}
        </div>

        <form className="comment-form" onSubmit={submit}>
          <Avatar username={user?.username} url={user?.avatar_url} size="small" />
          <input
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Viết bình luận..."
            aria-label="Nội dung bình luận"
          />
          <button className="primary">Gửi</button>
        </form>
      </section>
    </main>
  );
}
