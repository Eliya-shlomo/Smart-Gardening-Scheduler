import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity, Alert, StyleSheet, ActivityIndicator, ScrollView } from "react-native";
import axios from "axios";
import { useRouter } from "expo-router";
import { useAuth } from "../context/AuthContext";
import { BASE_URL_CLIENTS } from "../context/config";

export default function DeleteClientScreen() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    axios.get(`${BASE_URL_CLIENTS}/clients/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setClients(res.data))
    .catch(err => console.log(err))
    .finally(() => setLoading(false));
  }, []);

  const handleDelete = (clientId: number, clientName: string) => {
    Alert.alert(
      "Confirm Delete",
      `Are you sure you want to delete "${clientName}"?`,
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: async () => {
            try {
              await axios.delete(`${BASE_URL_CLIENTS}/clients/${clientId}`, {
                headers: { Authorization: `Bearer ${token}` },
              });
              Alert.alert("Client deleted successfully");
              router.push("/clients")
            } catch (err) {
              Alert.alert("Error", "Failed to delete client.");
              console.log(err);
            }
          },
        },
      ]
    );
  };

  if (loading) return <ActivityIndicator size="large" style={{ marginTop: 100 }} />;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Delete Clients</Text>

      {clients.map((client: any) => (
        <View key={client.id} style={styles.clientRow}>
          <View>
            <Text style={styles.clientName}>{client.name}</Text>
            <Text style={styles.clientAddress}>{client.address}</Text>
          </View>
          <TouchableOpacity
            style={styles.deleteButton}
            onPress={() => handleDelete(client.id, client.name)}
          >
            <Text style={styles.deleteButtonText}>Delete</Text>
          </TouchableOpacity>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: "#27ae60",
  },
  clientRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#d5f5e3",
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: "#27ae60",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  clientName: {
    fontSize: 18,
    color: "#145a32",
    fontWeight: "600",
  },
  clientAddress: {
    fontSize: 14,
    color: "#7f8c8d",
  },
  deleteButton: {
    backgroundColor: "#e74c3c",
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  deleteButtonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
  },
});
