import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  SafeAreaView,
} from "react-native";
import { useRouter, useLocalSearchParams, Stack } from "expo-router";
import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BASE_URL_APPOINTMENTS } from "@/context/config";

type Appointment = {
  id: number;
  date: string;
  time: string;
  treatment_type: string;
  status: string;
  notes?: string;
};



export default function AppointmentsScreen() {
  const { id, name } = useLocalSearchParams<{ id: string; name?: string }>();
  const router = useRouter();

  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const token = await AsyncStorage.getItem("token");
        if (!token || !id) {
          setError("Unauthorized");
          setLoading(false);
          return;
        }

        const res = await axios.get(
          `${BASE_URL_APPOINTMENTS}/appointments/client/${id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );


        const sortedAppointments = res.data.sort((a: Appointment, b: Appointment) => {
          const dateA = new Date(`${a.date.split("T")[0]}T${a.time}`);
          const dateB = new Date(`${b.date.split("T")[0]}T${b.time}`);
          return dateA.getTime() - dateB.getTime(); 
        });
        
        setAppointments(sortedAppointments);
        setError(null);
      } catch (err: any) {
        console.error("Error fetching appointments:", err?.response?.data || err.message);
        setError("Failed to load appointments.");
      } finally {
        setLoading(false);
      }
    };

    fetchAppointments();
  }, [id]);
  const decodedName = decodeURIComponent(name || "Client");

  const handleAddMeeting = () => {
    const encodedName = encodeURIComponent(name || "");
    router.push(`/clients/${id}/create-meeting?name=${encodedName}`);
  };


  return (
    <>
    <Stack.Screen options={{ title: `Appointments` }} />
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Appointments for {decodedName}</Text>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color="#3498db" />
        </View>
      ) : error ? (
        <View style={styles.center}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      ) : appointments.length === 0 ? (
        <View style={styles.center}>
          <Text style={styles.noAppointmentsText}>No appointments found.</Text>
        </View>
      ) : (
        <FlatList
          data={appointments}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.text}>📅 {item.date.slice(0, 10)} ⏰ {item.time}</Text>
              <Text style={styles.text}>🌿 {item.treatment_type}</Text>
              <Text style={styles.text}>📋 {item.status}</Text>
              {<Text style={styles.text}>📝 {item.notes}</Text>}
            </View>
          )}
          contentContainerStyle={{ paddingBottom: 80 }}
        />
      )}
      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.addButtonFixed} onPress={handleAddMeeting}>
          <Text style={styles.addButtonText}>+ Add New Meeting</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.addButtonFixed} onPress={handleAddMeeting}>
          <Text style={styles.addButtonText}>- Delete Meeting</Text>
        </TouchableOpacity>
      </View>
      
    </SafeAreaView>
    </>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
  },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: "#2c3e50",
  },
  card: {
    backgroundColor: "#ecf0f1",
    padding: 16,
    borderRadius: 12,
    marginBottom: 15,
    shadowColor: "#7f8c8d",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  text: {
    fontSize: 16,
    color: "#2c3e50",
    marginBottom: 4,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  noAppointmentsText: {
    fontSize: 18,
    color: "#7f8c8d",
    textAlign: "center",
  },
  errorText: {
    fontSize: 18,
    color: "red",
    textAlign: "center",
    marginBottom: 10,
  },
  addButtonFixed: {
    bottom: 25,
    backgroundColor: "#27ae60",
    paddingVertical: 15,
    borderRadius: 25,
    alignItems: "center",
    elevation: 5,
    width: "50%",
  },
  addButtonText: {
    color: "white",
    fontSize: 18,
    fontWeight: "700",
  },
  buttonRow:{
    position: "absolute",
  bottom: 25,
  left: 20,
  right: 20,
  flexDirection: "row",
  justifyContent: "center",
  alignItems: "center",
  gap: 15,
  },
});

