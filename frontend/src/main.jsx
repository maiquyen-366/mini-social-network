// Tầng entrypoint: mount React app và nạp CSS thuần.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";
import "./styles/profile.css";
import "./styles/chat.css";
import "./styles/theme.css";
import "./styles/notifications.css";

createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
