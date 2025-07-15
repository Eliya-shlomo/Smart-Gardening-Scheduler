import React, { createContext, useState, ReactNode, useContext } from "react";

type AuthContextType = {
  isConnected: boolean;
  login: () => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);

  const login = () => setIsConnected(true);
  const logout = () => setIsConnected(false);

  return (
    <AuthContext.Provider value={{ isConnected, login, logout }}>
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
