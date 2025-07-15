import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useAuth } from "../context/AuthContext";
import { useRouter } from "expo-router";

export const options = {
  headerBackVisible: false,
};

export default function WelcomeScreen() {
  const { login } = useAuth();
  const router = useRouter();

  const onSignInPress = () => {
    router.push("/login");
  };

  const onRegisterPress = () => {
    router.push("/register");
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={[styles.button, styles.signIn]} onPress={onSignInPress}>
        <Text style={styles.buttonText}>Sign In</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.button, styles.register]} onPress={onRegisterPress}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",  
    alignItems: "center",      
    paddingHorizontal: 20,
    backgroundColor: "#fff",
  },
  button: {
    width: "80%",              
    paddingVertical: 15,
    borderRadius: 8,
    marginBottom: 20,
    alignItems: "center",
  },
  signIn: {
    backgroundColor: "#3498db",
  },
  register: {
    backgroundColor: "#2ecc71",
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "600",
  },
});
