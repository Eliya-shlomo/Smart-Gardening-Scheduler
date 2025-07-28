import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
  Platform,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import DateTimePickerModal from "react-native-modal-datetime-picker";
import axios from "axios";
import { useAuth } from "@/context/AuthContext";
import { BASE_URL_APPOINTMENTS } from "@/context/config";

export default function CreateMeetingScreen() {
  const router = useRouter();
  const { token } = useAuth();
  const { id, name } = useLocalSearchParams<{ id: string; name?: string }>();

  const [date, setDate] = useState<Date | null>(null);
  const [time, setTime] = useState<Date | null>(null);
  const [treatmentType, setTreatmentType] = useState("");
  const [status, setStatus] = useState<"pending" | "done">("pending");
  const [notes, setNotes] = useState("");

  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
  const [isTimePickerVisible, setTimePickerVisibility] = useState(false);
  const [showStatusDropdown, setShowStatusDropdown] = useState(false);

  const handleConfirmDate = (selectedDate: Date) => {
    setDate(selectedDate);
    setDatePickerVisibility(false);
  };

  const handleConfirmTime = (selectedTime: Date) => {
    setTime(selectedTime);
    setTimePickerVisibility(false);
  };

  const handleSubmit = async () => {
    if (!date || !time || !treatmentType || !notes || !status) {
      Alert.alert("Please fill all required fields.");
      return;
    }

    const formattedDate = date.toISOString().split("T")[0];
    const formattedTime = time.toTimeString().split(":").slice(0, 2).join(":");
    


    try {
      await axios.post(
        `${BASE_URL_APPOINTMENTS}/appointments/`,
        {
          client_id: parseInt(id),
          date: formattedDate,
          time: formattedTime,
          treatment_type: treatmentType,
          notes,
          status,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      Alert.alert("Meeting created successfully!");
      router.replace(`/clients/${id}/appointments?name=${encodeURIComponent(name || "")}`);
    } catch (err: any) {
      console.error("Error creating appointment:", err.response?.data || err.message);
      Alert.alert("Failed to create meeting");
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Create Meeting for {name || "Client"}</Text>

      {/* Date Picker */}
      <TouchableOpacity onPress={() => setDatePickerVisibility(true)} style={styles.input}>
        <Text style={{ color: date ? "#000" : "#888" }}>
          {date ? date.toISOString().split("T")[0] : "Select Date"}
        </Text>
      </TouchableOpacity>
      <DateTimePickerModal
        isVisible={isDatePickerVisible}
        mode="date"
        onConfirm={handleConfirmDate}
        onCancel={() => setDatePickerVisibility(false)}
      />

      {/* Time Picker */}
      <TouchableOpacity onPress={() => setTimePickerVisibility(true)} style={styles.input}>
        <Text style={{ color: time ? "#000" : "#888" }}>
          {time ? time.toTimeString().split(":").slice(0, 2).join(":") : "Select Time"}
        </Text>
      </TouchableOpacity>
      <DateTimePickerModal
        isVisible={isTimePickerVisible}
        mode="time"
        is24Hour={true}
        onConfirm={handleConfirmTime}
        onCancel={() => setTimePickerVisibility(false)}
      />

      {/* Treatment Type */}
      <TextInput
        style={styles.input}
        placeholder="Treatment Type"
        placeholderTextColor="#888"
        value={treatmentType}
        onChangeText={setTreatmentType}
      />

      {/* Status Dropdown */}
      <TouchableOpacity
        style={styles.input}
        onPress={() => setShowStatusDropdown(!showStatusDropdown)}
      >
        <Text style={{ color: "#000" }}>Status: {status}</Text>
      </TouchableOpacity>
      {showStatusDropdown && (
        <View style={styles.dropdown}>
          <TouchableOpacity
            onPress={() => {
              setStatus("pending");
              setShowStatusDropdown(false);
            }}
            
          >
            <Text style={styles.dropdownItem}>Pending</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => {
              setStatus("done");
              setShowStatusDropdown(false);
            }}
          >
            <Text style={styles.dropdownItem}>Done</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Notes */}
      <TextInput
        style={[styles.input, { height: 100 }]}
        placeholder="Notes"
        placeholderTextColor="#888"
        value={notes}
        onChangeText={setNotes}
        multiline
      />

      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Create</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 24,
    backgroundColor: "#fff",
    flexGrow: 1,
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 20,
    color: "#333",
    textAlign: "center",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    padding: 12,
    borderRadius: 8,
    marginBottom: 15,
    fontSize: 16,
    backgroundColor: "#f9f9f9",
  },
  button: {
    backgroundColor: "#27ae60",
    padding: 15,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
  },
  dropdown: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    backgroundColor: "#f9f9f9",
    marginBottom: 15,
  },
  dropdownItem: {
    padding: 12,
    fontSize: 16,
    color: "#333",
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },
});
