import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to the Home Page!</Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push("/clients")}
      >
        <Text style={styles.buttonText}>View Clients</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={() => router.push("/create-client")}
      >
        <Text style={styles.buttonText}>Create New Client</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 40,
    textAlign: "center",
  },
  button: {
    width: "80%",              // כפתור רחב ואחיד
    paddingVertical: 15,
    borderRadius: 8,
    backgroundColor: "#3498db",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 15,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "600",
  },
});
