// Tầng page: newsfeed mới nhất, tạo bài, like và xóa bài.
import PostCard from "../components/PostCard";
import PostForm from "../components/PostForm";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { usePosts } from "../hooks/usePosts";
import Avatar from "../components/Avatar";

export default function Feed() {
  const { user } = useAuth(); const { posts, pagination, addPost, removePost, likePost, loadMore } = usePosts();
  return <main className="feed-layout"><section className="feed-main"><div className="page-intro"><div><span className="eyebrow">CỘNG ĐỒNG</span><h1>Newsfeed</h1><p>Cập nhật mới nhất từ bạn bè của bạn.</p></div></div><PostForm user={user} onSubmit={addPost} /><section className="post-list">{posts.length ? posts.map((post) => <PostCard key={post.id} post={post} currentUser={user} onLike={likePost} onDelete={removePost} />) : <div className="card empty-state"><span className="empty-icon">✦</span><h2>Chưa có bài viết</h2><p>Hãy là người đầu tiên chia sẻ điều gì đó.</p></div>}{pagination.next && <button className="load-more" onClick={loadMore}>Tải thêm bài viết</button>}</section></section><aside className="feed-aside"><div className="card profile-mini"><Avatar username={user?.username} url={user?.avatar_url} size="large" /><h2>{user?.username}</h2><p>{user?.bio || "Hãy cập nhật hồ sơ để mọi người biết thêm về bạn."}</p><Link to="/profile">Xem hồ sơ →</Link></div><div className="card tip-card"><strong>Gợi ý nhỏ</strong><p>Chia sẻ điều tích cực và tôn trọng mọi người trong cộng đồng.</p></div></aside></main>;
}
