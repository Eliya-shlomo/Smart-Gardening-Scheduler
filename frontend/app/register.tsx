import React, { useState } from "react";
import axios from "axios";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
} from "react-native";
import { useAuth } from "../context/AuthContext";
import { useRouter } from "expo-router";

// For it to work you need to put the IP of the computer
const API_URL = "http://192.168.1.182:8000"


export default function RegisterScreen() {
  const { login } = useAuth();
  const router = useRouter();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    if (!fullName || !email || !phone || !password) {
      Alert.alert("Please fill out all fields");
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/users/register`, {
        name: fullName,
        email,
        phone,
        password,
      });

      Alert.alert("Registered successfully!");

      login(response.data); 
      router.push("/home");

    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        const serverMessage = error.response?.data?.detail;
      
        console.log("Axios Error:", error.response?.data);
      
        if (typeof serverMessage === "string") {
          Alert.alert("Registration failed", serverMessage);
        } else if (Array.isArray(serverMessage)) {
          const message = serverMessage.map((err: any) => err.msg).join("\n");
          Alert.alert("Registration failed", message);
        } else {
          Alert.alert("Registration failed", "Something went wrong. Please try again.");
        }
      } else {
        console.log("Unknown Error:", error);
        Alert.alert("Error", "Unexpected error occurred");
      }
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : undefined}
      style={{ flex: 1 }}
    >
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Create an Account</Text>

        <TextInput
          placeholder="Full Name"
          placeholderTextColor="#888"
          value={fullName}
          onChangeText={setFullName}
          style={styles.input}
        />

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
          placeholder="Phone"
          placeholderTextColor="#888"
          value={phone}
          onChangeText={setPhone}
          keyboardType="phone-pad"
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

        <TouchableOpacity style={styles.button} onPress={handleRegister}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 60,
    paddingHorizontal: 20,
    alignItems: "center",
    backgroundColor: "#fff",
    flexGrow: 1,
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
    backgroundColor: "#2ecc71",
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
