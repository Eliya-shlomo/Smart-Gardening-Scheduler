import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, ScrollView } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import axios from "axios";
import { useAuth } from "@/context/AuthContext";
import { BASE_URL_CLIENTS } from "../../context/config";

type Client = {
  id: number;
  name: string;
  phone: string;
  address: string;
  email: string;
};

export default function ClientDetailsScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { token } = useAuth();
  const router = useRouter();

  const [client, setClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchClient = async () => {
      try {
        const res = await axios.get(`${BASE_URL_CLIENTS}/clients/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setClient(res.data);
      } catch (err) {
        console.error("Error fetching client:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchClient();
  }, [id, token]);

  const handleViewMeetings = () => router.push(`/clients/${id}/meetings`);
  const handleCreateMeeting = () => router.push(`/clients/${id}/create-meeting`);
  const handleViewTrees = () => router.push(`/clients/${id}/trees`);
  const handleCreateTree = () => router.push(`/clients/${id}/create-tree`);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  if (!client) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Failed to load client information.</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.clientInfo}>
        <Text style={styles.title}>{client.name}</Text>
        <Text style={styles.detail}>📞 {client.phone}</Text>
        <Text style={styles.detail}>🏠 {client.address}</Text>
        <Text style={styles.detail}>✉️ {client.email}</Text>
      </View>

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
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: "#fff",
    alignItems: "center",
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  clientInfo: {
    width: "100%",
    backgroundColor: "#d0e8ff",       
    padding: 24,                      
    borderRadius: 16,                 
    marginBottom: 30,
    shadowColor: "#007aff",           
    shadowOpacity: 0.3,               
    shadowRadius: 10,                 
    shadowOffset: { width: 0, height: 4 },
    elevation: 8,                    
  },
  
  title: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 10,
    color: "#333",
  },
  detail: {
    fontSize: 16,
    color: "#555",
    marginBottom: 6,
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
  errorText: {
    fontSize: 18,
    color: "red",
  },
});
