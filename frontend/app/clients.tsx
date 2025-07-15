import React from "react";
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from "react-native";
import { useRouter } from "expo-router";

// דוגמה של לקוחות. בהמשך תוכל לטעון מ-API.
const clients = [
  { id: "1", name: "John Doe" },
  { id: "2", name: "Jane Smith" },
  { id: "3", name: "David Cohen" },
];

export default function ClientsScreen() {
  const router = useRouter();

  const renderItem = ({ item }: { item: { id: string; name: string } }) => {
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
  
  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Clients</Text>
      <FlatList
        data={clients}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: "#fff" },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 20, textAlign: "center" },
  item: {
    padding: 15,
    backgroundColor: "#ecf0f1",
    borderRadius: 8,
    marginBottom: 12,
  },
  itemText: { fontSize: 18 },
});
