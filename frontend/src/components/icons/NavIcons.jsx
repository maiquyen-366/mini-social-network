// Tầng component: các icon SVG nhỏ dùng chung cho navbar và chat.
function IconFrame({ children, className = "" }) {
  return (
    <svg
      className={`ui-icon ${className}`.trim()}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.9"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

export function HomeIcon() {
  return <IconFrame><path d="m3 10 9-7 9 7" /><path d="M5 9.5V21h14V9.5" /><path d="M9 21v-7h6v7" /></IconFrame>;
}

export function ChatIcon() {
  return <IconFrame><path d="M21 15a4 4 0 0 1-4 4H8l-5 3 1.7-5A7 7 0 0 1 3 12V8a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z" /></IconFrame>;
}

export function BellIcon() {
  return <IconFrame><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 21h4" /></IconFrame>;
}

export function SunIcon() {
  return <IconFrame><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41" /></IconFrame>;
}

export function MoonIcon() {
  return <IconFrame><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5 8.5 8.5 0 1 0 20.5 14.5Z" /></IconFrame>;
}

export function LogoutIcon() {
  return <IconFrame><path d="M10 17l5-5-5-5M15 12H3" /><path d="M14 3h5a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-5" /></IconFrame>;
}

export function SendIcon() {
  return <IconFrame><path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" /></IconFrame>;
}

export function SmileIcon() {
  return <IconFrame><circle cx="12" cy="12" r="9" /><path d="M8.5 10h.01M15.5 10h.01M8 14.5a5.2 5.2 0 0 0 8 0" /></IconFrame>;
}
