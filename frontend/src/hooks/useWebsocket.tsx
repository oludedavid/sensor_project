/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useRef, useState } from "react";

const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<string[]>([]);
  const [jsonData, setJsonData] = useState<any>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        setIsConnected(true);
        setError(null);
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setJsonData(data);
          setMessages((prev) => [...prev, JSON.stringify(data)]);
        } catch {
          setMessages((prev) => [...prev, event.data]);
        }
      };

      ws.current.onerror = () => {
        setError("WebSocket error");
      };

      ws.current.onclose = () => {
        setIsConnected(false);
        setError("WebSocket connection closed");
      };
    } catch (e: any) {
      setError(`WebSocket error: ${e.message}`);
      return;
    }

    return () => {
      ws.current?.close();
    };
  }, [url]);

  const sendMessage = (messages: string[]) => {
    if (ws.current && isConnected) {
      messages.forEach((message) => {
        ws.current?.send(message);
      });
    } else {
      setError("WebSocket is not connected");
    }
  };

  const sendJsonData = (data: any) => {
    if (ws.current && isConnected && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    } else {
      setError("WebSocket is not connected");
    }
  };

  return { isConnected, messages, jsonData, error, sendMessage, sendJsonData };
};

export default useWebSocket;
