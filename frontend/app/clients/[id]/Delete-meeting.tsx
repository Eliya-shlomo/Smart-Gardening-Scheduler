import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity, Alert, StyleSheet, ActivityIndicator, ScrollView } from "react-native";
import axios from "axios";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useAuth } from "@/context/AuthContext";
import { BASE_URL_APPOINTMENTS } from "@/context/config";

export default function DeleteMeetingScreen() {
    const [meetings, setMeetings] = useState([]);
    const [loading, setLoading] = useState(true);
    const { token } = useAuth();
    const router = useRouter();
    const { id, name } = useLocalSearchParams<{ id: string; name?: string }>();
    


    useEffect(() => {
        axios.get(`${BASE_URL_APPOINTMENTS}/appointments/client/${id}`,{
        headers: { Authorization: `Bearer ${token}` },
        })
        .then(res => setMeetings(res.data))
        .catch(err => console.log(err))
        .finally(() => setLoading(false));
    }, []);

    if (loading) return <ActivityIndicator size="large" style={{ marginTop: 100 }} />;


    

    function handleDelete(meetingId: any, date: any, time: any): void {
            Alert.alert(
              "Confirm Delete",
              `Are you sure you want to delete the meeting on ${date} at ${time}?`,
              [

                { text: "Cancel", style: "cancel" },
                {
                    text: "Delete",
                    style: "destructive",
                    onPress: async () => {
                      try {
                        await axios.delete(`${BASE_URL_APPOINTMENTS}/appointments/${meetingId}`, {
                          headers: { Authorization: `Bearer ${token}` },
                        });
                        Alert.alert("Meeting deleted successfully");
                        router.push("/clients")
                      } catch (err) {
                        Alert.alert("Error", "Failed to delete meeting.");
                        console.log(err);
                      }
                    },
                  },
              ]
            );
    }

    return (
        <ScrollView contentContainerStyle={styles.container}>
          <Text style={styles.title}>Delete Meetings</Text>
    
          {meetings.map((meeting: any) => (
            <View key={meeting.id} style={styles.meetingRow}>
              <View>
                <Text style={styles.text}>📅 {meeting.date.slice(0, 10)} ⏰ {meeting.time}</Text>
                <Text style={styles.text}>🌿 {meeting.treatment_type}</Text>
                <Text style={styles.text}>📋 {meeting.status}</Text>
                {<Text style={styles.text}>📝 {meeting.notes}</Text>}
              </View>
              <TouchableOpacity
                style={styles.deleteButton}
                onPress={() => handleDelete(meeting.id, meeting.date.slice(0, 10), meeting.time)}
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
    meetingRow: {
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
    text: {
        fontSize: 16,
        color: "#2c3e50",
        marginBottom: 4,
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


