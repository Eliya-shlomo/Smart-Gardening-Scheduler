import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  SafeAreaView,
} from "react-native";
import { useRouter } from "expo-router";
import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

import { BASE_URL_CLIENTS } from "../context/config";

type Client = {
  id: number;
  name: string;
  address?: string;
  phone?: string;
};

export default function ClientsScreen() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const token = await AsyncStorage.getItem("token");
        if (!token) {
          setError("Please reconnect.");
          setLoading(false);
          return;
        }

        const res = await axios.get(`${BASE_URL_CLIENTS}/clients/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        setClients(res.data);
        setError(null);
      } catch (error: any) {
        console.error("Error fetching clients:", error?.response?.data || error.message);
        setError("There is a problem uploading clients.");
      } finally {
        setLoading(false);
      }
    };

    fetchClients();
  }, []);

  const renderItem = ({ item }: { item: Client }) => {
    const encodedName = encodeURIComponent(item.name);
    return (
      <TouchableOpacity
        style={styles.item}
        onPress={() => router.push(`/clients/${item.id}?name=${encodedName}`)}
      >
        <Text style={styles.itemText}>{item.name}</Text>
      </TouchableOpacity>
    );
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.center]}>
        <ActivityIndicator size="large" color="#2ecc71" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.container, styles.center]}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity
          style={styles.addButton}
          onPress={() => router.push("/create-client")}
        >
          <Text style={styles.addButtonText}>Add a new client</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Clients</Text>

      {clients.length === 0 ? (
        <View style={styles.center}>
          <Text style={styles.noClientsText}>You don't have any clients yet.</Text>
        </View>
      ) : (
        <FlatList
          data={clients}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 80 }}
        />
      )}

      <TouchableOpacity
        style={styles.addButtonFixed}
        onPress={() => router.push("/create-client")}
      >
        <Text style={styles.addButtonText}>+ Add New Client</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
  },
  center: {
    justifyContent: "center",
    alignItems: "center",
    flex: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: "#27ae60",
  },
  item: {
    padding: 15,
    backgroundColor: "#d5f5e3",
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: "#27ae60",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  itemText: {
    fontSize: 18,
    color: "#145a32",
    fontWeight: "600",
  },
  errorText: {
    color: "#e74c3c",
    fontSize: 18,
    marginBottom: 20,
    textAlign: "center",
    fontWeight: "600",
  },
  noClientsText: {
    fontSize: 20,
    marginBottom: 20,
    textAlign: "center",
    color: "#34495e",
  },
  addButton: {
    backgroundColor: "#27ae60",
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 25,
    elevation: 3,
  },
  addButtonFixed: {
    position: "absolute",
    bottom: 25,
    left: 20,
    right: 20,
    backgroundColor: "#27ae60",
    paddingVertical: 15,
    borderRadius: 25,
    alignItems: "center",
    elevation: 5,
  },
  addButtonText: {
    color: "white",
    fontSize: 18,
    fontWeight: "700",
  },
});
