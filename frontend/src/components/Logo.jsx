// Tầng component: hiển thị logo SVG chính thức của Mini Social.
export default function Logo({ className = "" }) {
  return (
    <img
      className={`app-logo ${className}`.trim()}
      src="/favicon.svg"
      width="36"
      height="36"
      alt=""
      aria-hidden="true"
    />
  );
}
