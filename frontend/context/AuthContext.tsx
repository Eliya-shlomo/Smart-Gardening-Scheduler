import React, { createContext, useState, ReactNode, useContext, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

type User = {
  id?: number;
  name?: string;
  email?: string;
  phone?: string;
};

type AuthContextType = {
  isConnected: boolean;
  user: User | null;
  token: string | null;
  login: (userData: User, token: string) => void; 
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const login = async (userData: User, token: string) => {
    setIsConnected(true);
    setUser(userData);
    setToken(token);
    await AsyncStorage.setItem("token", token);
  };

  const logout = async () => {
    setIsConnected(false);
    setUser(null);
    setToken(null);
    await AsyncStorage.removeItem("token");
  };

  useEffect(() => {
    const loadFromStorage = async () => {
      const savedToken = await AsyncStorage.getItem("token");
      if (savedToken) {
        try {
          const res = await axios.get("http://192.168.1.182:8000/users/me", {
            headers: { Authorization: `Bearer ${savedToken}` },
          });
          setUser(res.data);
          setToken(savedToken);
          setIsConnected(true);
        } catch (err) {
          console.log("Invalid or expired token", err);
          await AsyncStorage.removeItem("token");
        }
      }
    };
    loadFromStorage();
  }, []);

  return (
    <AuthContext.Provider value={{ isConnected, user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
