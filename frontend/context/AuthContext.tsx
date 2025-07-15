import React, { createContext, useState, ReactNode, useContext } from "react";

type User = {
  id?: number;
  name?: string;
  email?: string;
  phone?: string;
};

type AuthContextType = {
  isConnected: boolean;
  user: User | null;
  login: (userData: User) => void; 
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const login = (userData: User) => {
    setIsConnected(true);
    setUser(userData);
  };

  const logout = () => {
    setIsConnected(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isConnected, user, login, logout }}>
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
