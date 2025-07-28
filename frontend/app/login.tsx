import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { useRouter } from "expo-router";
import { BASE_URL_USERS } from "../context/config";
import axios from "axios";


export default function LoginScreen() {
  const { login } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignIn = async () => {
    if (!email || !password) {
      Alert.alert("Please enter both email and password.");
      return;
    }
    try {
      const response = await axios.post(`${BASE_URL_USERS}/users/login`, {
        email,
        password,
      });
  
      const token = response.data.access_token;
  
      const userRes = await axios.get(`${BASE_URL_USERS}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
  
  
      login(userRes.data, token);
      router.push("/home");
  
    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        const serverMessage = error.response?.data?.detail;
        console.log("Axios Error:", error.response?.data);
  
        if (typeof serverMessage === "string") {
          Alert.alert("login failed", serverMessage);
        } else if (Array.isArray(serverMessage)) {
          const message = serverMessage.map((err: any) => err.msg).join("\n");
          Alert.alert("login failed", message);
        } else {
          Alert.alert("login failed", "Something went wrong. Please try again.");
        }
      } else {
        console.log("Unknown Error:", error);
        Alert.alert("Error", "Unexpected error occurred");
      }
    }
  };
  

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.container}>
        <Text style={styles.title}>Sign In</Text>

        <TextInput
          placeholder="Email"
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          style={styles.input}
        />

        <TextInput
          placeholder="Password"
          placeholderTextColor="#888"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          style={styles.input}
        />

        <TouchableOpacity style={styles.button} onPress={handleSignIn}>
          <Text style={styles.buttonText}>Sign In</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 80,
    paddingHorizontal: 20,
    backgroundColor: "#fff",
    alignItems: "center",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 40,
  },
  input: {
    width: "100%",
    height: 50,
    borderColor: "#ccc",
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 20,
    fontSize: 16,
  },
  button: {
    backgroundColor: "#3498db",
    paddingVertical: 15,
    borderRadius: 8,
    width: "100%",
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "600",
  },
});
