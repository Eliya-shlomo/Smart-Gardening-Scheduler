import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";

export default function ClientDetailsScreen() {
  const router = useRouter();
  const { id, name } = useLocalSearchParams();


  const handleViewMeetings = () => {
    router.push(`/clients/${id}/meetings`);
  };

  const handleCreateMeeting = () => {
    router.push(`/clients/${id}/create-meeting`);
  };

  const handleViewTrees = () => {
    router.push(`/clients/${id}/trees`);
  };

  const handleCreateTree = () => {
    router.push(`/clients/${id}/create-tree`);
  };

  return (
    <View style={styles.container}>
    <Text style={styles.title}>Client: {name}</Text>

    <Text style={styles.subtitle}>Client ID: {id}</Text>

      <TouchableOpacity style={styles.button} onPress={handleViewMeetings}>
        <Text style={styles.buttonText}>View Meetings</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={handleCreateMeeting}>
        <Text style={styles.buttonText}>Create New Meeting</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={handleViewTrees}>
        <Text style={styles.buttonText}>View Trees</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={handleCreateTree}>
        <Text style={styles.buttonText}>Add New Tree</Text>
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
  subtitle: {
    fontSize: 20,
    color: "#555",
    fontWeight: "bold",
    marginBottom: 20,
    
  },
  title: {
    fontSize: 20,
    color: "#555",
    fontWeight: "bold",
    marginBottom: 40,
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
    fontSize: 16,
    fontWeight: "600",
  },
});
