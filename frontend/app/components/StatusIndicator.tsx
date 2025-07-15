import React from "react";
import { View, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useAuth } from "../../context/AuthContext";
import { useRouter } from "expo-router";

export default function StatusIndicator() {
  const { isConnected, logout } = useAuth();
  const router = useRouter();

  const handlePress = () => {
    if (!isConnected) return;

    Alert.alert(
      "Logout",
      "Are you sure you want to log out?",
      [
        {
          text: "Cancel",
          style: "cancel",
        },
        {
          text: "Logout",
          style: "destructive",
          onPress: () => {
            logout();
            router.replace("/");
          },
        },
      ],
      { cancelable: true }
    );
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={handlePress}
        style={[
          styles.circle,
          { backgroundColor: isConnected ? "#2ecc71" : "#bdc3c7" },
        ]}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: "absolute",
    top: 40,
    right: 20,
    zIndex: 1000, 
    elevation: 10, 
  },
  circle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: "#fff",
    backgroundColor: "#bdc3c7",
    cursor: "pointer", 
  },
});

