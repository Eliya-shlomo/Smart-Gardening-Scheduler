import React, { useEffect } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Stack, useRouter } from "expo-router";
import { useAuth } from "@/context/AuthContext";

export default function HomeScreen() {
  const router = useRouter();
  const { user, token } = useAuth();

  useEffect(() => {
    if (!token) {
      const timeout = setTimeout(() => {
        router.replace("/");
      }, 2000); 
  
      return () => clearTimeout(timeout); 
    }
  }, [token]);

  if (!token) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Checking authentication...</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          headerLeft: () => <></>,
        }}
      />
      <View style={styles.container}>
        <Text style={styles.title}>
          Welcome{user?.name ? `, ${user.name}` : "!"}
        </Text>

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
    </>
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
    width: "80%",
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
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  }
});
