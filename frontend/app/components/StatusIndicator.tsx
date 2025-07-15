import React from "react";
import { View, TouchableOpacity, StyleSheet, Text, Alert } from "react-native";
import { useAuth } from "../../context/AuthContext";
import { useRouter } from "expo-router";

export default function StatusIndicator() {
  const { isConnected, logout } = useAuth();
  const { user } = useAuth(); 
  const userName = user?.name ?? "";

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

  // The first letter of the name is capitalized, or blank if there is no name.
  const firstLetter = userName ? userName.charAt(0).toUpperCase() : "";

  return (
    <View style={styles.container}>
      <TouchableOpacity
        onPress={handlePress}
        style={[
          styles.circle,
          { backgroundColor: isConnected ? "#2ecc71" : "#bdc3c7" },
        ]}
      >
        {isConnected && (
          <Text style={styles.letter}>
            {firstLetter}
          </Text>
        )}
      </TouchableOpacity>
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
    width: 32,
    height: 32,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: "#fff",
    backgroundColor: "#bdc3c7",
    justifyContent: "center",
    alignItems: "center",
  },
  letter: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 18,
  },
});
