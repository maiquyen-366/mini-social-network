// Tầng component: hiển thị bảng emoji Unicode và trả emoji được chọn.
import { useEffect, useRef, useState } from "react";
import { SmileIcon } from "./icons/NavIcons";

const EMOJI_GROUPS = [
  { name: "Cảm xúc", emojis: ["😀", "😄", "😁", "😂", "😊", "😍", "🥰", "😎", "🤔", "😢", "😭", "😴"] },
  { name: "Cử chỉ", emojis: ["👍", "👎", "👏", "🙌", "🙏", "👌", "✌️", "🤝", "💪", "👋"] },
  { name: "Trái tim", emojis: ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "💖", "💔"] },
  { name: "Hoạt động", emojis: ["🎉", "✨", "🔥", "🎂", "🎁", "⚽", "🎮", "🎵", "📚", "☕"] },
];

export default function EmojiPicker({
  onSelect,
  disabled = false,
  className = "",
  ariaLabel = "Chọn emoji",
  title = "Chọn emoji",
}) {
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);
  const buttonRef = useRef(null);

  useEffect(() => {
    if (!open) return undefined;

    const closeFromOutside = (event) => {
      if (!wrapperRef.current?.contains(event.target)) setOpen(false);
    };
    const closeFromKeyboard = (event) => {
      if (event.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };

    document.addEventListener("pointerdown", closeFromOutside);
    document.addEventListener("keydown", closeFromKeyboard);
    return () => {
      document.removeEventListener("pointerdown", closeFromOutside);
      document.removeEventListener("keydown", closeFromKeyboard);
    };
  }, [open]);

  const selectEmoji = (emoji) => {
    onSelect(emoji);
  };

  return (
    <div className={`emoji-picker ${className}`.trim()} ref={wrapperRef}>
      <button
        ref={buttonRef}
        type="button"
        className={`chat-tool-button ${open ? "active" : ""}`}
        aria-label={ariaLabel}
        aria-expanded={open}
        title={title}
        disabled={disabled}
        onClick={() => setOpen((value) => !value)}
      >
        <SmileIcon />
      </button>

      {open && (
        <div className="emoji-picker-panel" role="dialog" aria-label="Bảng chọn emoji">
          {EMOJI_GROUPS.map((group) => (
            <section className="emoji-group" key={group.name}>
              <strong>{group.name}</strong>
              <div className="emoji-grid">
                {group.emojis.map((emoji) => (
                  <button
                    type="button"
                    className="emoji-option"
                    title={emoji}
                    aria-label={`Chèn emoji ${emoji}`}
                    onClick={() => selectEmoji(emoji)}
                    key={emoji}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
