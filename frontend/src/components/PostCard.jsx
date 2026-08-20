// Tầng component: hiển thị một bài đăng và thao tác like/xóa.
import { Link } from "react-router-dom";
import { useState } from "react";
import Avatar from "./Avatar";

export default function PostCard({ post, currentUser, onLike, onDelete }) {
  const [imageFailed, setImageFailed] = useState(false);
  const likeLabel = post.is_liked ? "Bỏ thích bài viết" : "Thích bài viết";

  return (
    <article className="card post-card">
      <div className="post-author">
        <Avatar username={post.author_username} url={post.author_avatar_url} />
        <div>
          <strong>{post.author_username}</strong>
          <small>{new Date(post.created_at).toLocaleString("vi-VN")}</small>
        </div>
      </div>

      <p className="post-content">{post.content}</p>

      {post.image_url && !imageFailed && (
        <img
          className="post-image"
          src={post.image_url}
          alt="Ảnh bài đăng"
          onError={() => setImageFailed(true)}
        />
      )}

      <div className="post-actions">
        <button
          type="button"
          className={`like-button ${post.is_liked ? "liked" : ""}`}
          onClick={() => onLike(post.id)}
          aria-pressed={Boolean(post.is_liked)}
          aria-label={likeLabel}
          title={likeLabel}
        >
          <svg
            className="like-icon"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M12 21s-7.2-4.35-9.55-8.55C.42 8.82 2.2 4.5 6.35 4.5c2.18 0 3.55 1.25 4.35 2.38.8-1.13 2.17-2.38 4.35-2.38 4.15 0 5.93 4.32 3.9 7.95C19.2 16.65 12 21 12 21Z" />
          </svg>
          <span className="like-count">{post.likes_count ?? 0}</span>
        </button>

        <Link to={`/posts/${post.id}`}>
          💬 {post.comments_count || 0} bình luận
        </Link>

        {currentUser?.id === post.author && (
          <button type="button" onClick={() => onDelete(post.id)}>
            Xóa
          </button>
        )}
      </div>
    </article>
  );
}
