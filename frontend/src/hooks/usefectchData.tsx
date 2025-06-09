import { useState } from "react";
import axios, { AxiosError } from "axios";
import { getCookie } from "cookies-next";

export default function useApiRequest<T = Record<string, unknown>>() {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<AxiosError | null>(null);
  const [loading, setLoading] = useState(false);

  const execute = async ({
    url,
    method,
    payload,
    requiresAuth = false,
  }: {
    url: string;
    method: "POST" | "GET" | "PUT" | "DELETE";
    payload?: Record<string, unknown>;
    requiresAuth?: boolean;
  }) => {
    setLoading(true);
    setError(null);

    try {
      const headers: Record<string, string> = {};

      if (requiresAuth) {
        const token = getCookie("access-token");
        if (!token) throw new Error("Missing authentication token");
        headers.Authorization = `Bearer ${token}`;
      }

      const config = {
        method,
        url,
        headers,
        ...(method === "GET" && payload
          ? { params: payload }
          : { data: payload }),
      };

      const response = await axios(config);
      setData(response.data);
      return response.data;
    } catch (err) {
      const error = err as AxiosError;
      setError(error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, execute };
}
