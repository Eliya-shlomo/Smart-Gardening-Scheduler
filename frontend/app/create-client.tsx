import React, { useState } from "react";
import {
  View,
  TextInput,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from "react-native";
import { Stack, useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

import { BASE_URL_CLIENTS } from "../context/config";

export default function CreateClientScreen() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name || !email || !address || !phone) {
      Alert.alert("Error", "Please fill in all fields");
      return;
    }

    setLoading(true);
    try {
      const token = await AsyncStorage.getItem("token");
      if (!token) {
        Alert.alert("Error", "please reconnect.");
        setLoading(false);
        return;
      }

      
      await axios.post(
        `${BASE_URL_CLIENTS}/clients/`,
        {
          name,
          email,
          address,
          phone,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      Alert.alert("The client was created successfully!");
      router.replace("/home");
    } catch (error: any) {
      console.error("Error creating client:", error.response?.data || error.message);
      Alert.alert("Error", "There was a problem creating the client, please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    <Stack.Screen options={{ title: "Create Client" }} />

    <View style={styles.container}>
      <Text style={styles.title}>Create a new Client</Text>

      <TextInput
        placeholder="Full name"
        placeholderTextColor="#888"
        value={name}
        onChangeText={setName}
        style={styles.input}
      />
      <TextInput
        placeholder="Email"
        placeholderTextColor="#888"
        value={email}
        onChangeText={setEmail}
        style={styles.input}
        keyboardType="email-address"
      />
      <TextInput
        placeholder="address"
        placeholderTextColor="#888"
        value={address}
        onChangeText={setAddress}
        style={styles.input}
      />
      <TextInput
        placeholder="phone"
        placeholderTextColor="#888"
        value={phone}
        onChangeText={setPhone}
        style={styles.input}
        keyboardType="phone-pad"
      />

      <TouchableOpacity
        style={[styles.button, loading && { backgroundColor: "#95c6a0" }]}
        onPress={handleSubmit}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Create a client</Text>
        )}
      </TouchableOpacity>
    </View>
    </>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
    justifyContent: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 30,
    textAlign: "center",
    color: "#27ae60",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
    fontSize: 16,
  },
  button: {
    backgroundColor: "#27ae60",
    padding: 15,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 18,
  },
});
