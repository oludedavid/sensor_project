/* eslint-disable react-hooks/exhaustive-deps */
import { createContext, useContext, useEffect, useState } from "react";
import useApiRequest from "@/hooks/usefectchData";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type User = {
  user_id: number;
  role: "admin" | "user";
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  setUser: (user: User | null) => void;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  loading: true,
  setUser: () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { execute, loading, data, error } = useApiRequest<User>();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (API_URL) {
          await execute({
            url: `${API_URL}/users/me`,
            requiresAuth: true,
            method: "GET",
          });
        }
      } catch (e) {
        console.error("Auth check failed:", e);
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (data) {
      setUser(data);
    } else if (error) {
      setUser(null);
    }
  }, [data, error]);

  const contextValue: AuthContextType = {
    user,
    isAuthenticated: !!user,
    loading,
    setUser,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
