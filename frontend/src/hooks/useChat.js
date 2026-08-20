// Tầng hook: quản lý REST history, room socket và sidebar socket realtime.
import { useCallback, useEffect, useRef, useState } from "react";
import {
  createChatSidebarSocket,
  createChatSocket,
  listConversations,
  listMessages,
} from "../services/chatService";

function mergeMessages(currentItems, incomingItems, readReceipts) {
  const byId = new Map();

  [...currentItems, ...incomingItems].forEach((message) => {
    const previous = byId.get(message.id);
    const receiptReadAt = readReceipts.get(message.id);
    const merged = { ...previous, ...message };

    if (previous?.is_read && !message.is_read) {
      merged.read_at = previous.read_at;
      merged.is_read = true;
    }
    if (receiptReadAt) {
      merged.read_at = receiptReadAt;
      merged.is_read = true;
    }
    byId.set(message.id, merged);
  });

  return [...byId.values()].sort((first, second) => (
    new Date(first.created_at) - new Date(second.created_at) || first.id - second.id
  ));
}

export const useChat = () => {
  const [conversations, setConversations] = useState([]);
  const [active, setActive] = useState(null);
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const [roomEnabled, setRoomEnabled] = useState(false);
  const roomSocketRef = useRef(null);
  const sidebarSocketRef = useRef(null);
  const sidebarReconnectTimerRef = useRef(null);
  const readReceiptsRef = useRef(new Map());

  const upsertConversation = useCallback((summary) => {
    setConversations((items) => [summary, ...items.filter((item) => item.id !== summary.id)]);
    setActive((current) => (current?.id === summary.id ? { ...current, ...summary } : current));
  }, []);

  useEffect(() => {
    listConversations().then((items) => {
      setConversations((current) => [
        ...current,
        ...items.filter((item) => !current.some((existing) => existing.id === item.id)),
      ]);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    let stopped = false;

    const connectSidebar = () => {
      if (stopped) return;

      let socket;
      try {
        socket = createChatSidebarSocket();
      } catch {
        sidebarReconnectTimerRef.current = setTimeout(connectSidebar, 2500);
        return;
      }

      sidebarSocketRef.current = socket;
      socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.type === "conversation.updated") upsertConversation(payload.data);
      };
      socket.onerror = () => socket.close();
      socket.onclose = (event) => {
        if (sidebarSocketRef.current === socket) sidebarSocketRef.current = null;
        if (!stopped && event.code !== 4001) {
          sidebarReconnectTimerRef.current = setTimeout(connectSidebar, 2500);
        }
      };
    };

    connectSidebar();
    return () => {
      stopped = true;
      clearTimeout(sidebarReconnectTimerRef.current);
      sidebarSocketRef.current?.close();
      sidebarSocketRef.current = null;
    };
  }, [upsertConversation]);

  useEffect(() => {
    const activeId = active?.id;
    if (!activeId || !roomEnabled) {
      setConnected(false);
      return undefined;
    }

    let stopped = false;
    setMessages([]);
    setConnected(false);

    listMessages(activeId).then((history) => {
      if (stopped) return;
      setMessages((current) => mergeMessages(
        history,
        current.filter((message) => message.conversation === activeId),
        readReceiptsRef.current,
      ));
    }).catch(() => {
      if (!stopped) setMessages([]);
    });

    const socket = createChatSocket(activeId);
    roomSocketRef.current = socket;
    socket.onopen = () => {
      if (!stopped) setConnected(true);
    };
    socket.onclose = () => {
      if (!stopped) setConnected(false);
    };
    socket.onerror = () => {
      if (!stopped) setConnected(false);
    };
    socket.onmessage = (event) => {
      if (stopped) return;
      const payload = JSON.parse(event.data);

      if (payload.type === "message.created" && payload.data.conversation === activeId) {
        setMessages((items) => mergeMessages(items, [payload.data], readReceiptsRef.current));
      }

      if (payload.type === "messages.read" && payload.data.conversation_id === activeId) {
        payload.data.message_ids.forEach((messageId) => {
          readReceiptsRef.current.set(messageId, payload.data.read_at);
        });
        const readIds = new Set(payload.data.message_ids);
        setMessages((items) => items.map((message) => (
          readIds.has(message.id)
            ? { ...message, read_at: payload.data.read_at, is_read: true }
            : message
        )));
      }
    };

    return () => {
      stopped = true;
      socket.close();
      if (roomSocketRef.current === socket) roomSocketRef.current = null;
      setConnected(false);
    };
  }, [active?.id, roomEnabled]);

  const openConversation = useCallback((conversation) => {
    setActive(conversation);
    setRoomEnabled(true);
  }, []);

  const deactivateRoom = useCallback(() => {
    roomSocketRef.current?.close();
    roomSocketRef.current = null;
    setConnected(false);
    setRoomEnabled(false);
  }, []);

  const sendMessage = (content) => {
    if (roomSocketRef.current?.readyState !== WebSocket.OPEN) return false;
    roomSocketRef.current.send(JSON.stringify({ content }));
    return true;
  };

  return {
    conversations,
    active,
    messages,
    connected,
    upsertConversation,
    openConversation,
    deactivateRoom,
    sendMessage,
  };
};
