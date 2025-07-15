import React from "react";
import { View, StyleSheet } from "react-native";
import { Stack } from "expo-router";
import { AuthProvider } from "../context/AuthContext";
import StatusIndicator from "./components/StatusIndicator";

export default function RootLayout() {
  return (
    <AuthProvider>
      <View style={styles.container}>
        <Stack>
          <Stack.Screen
            name="index"
            options={{
              headerBackVisible: false,
              headerLeft: () => <></>, 
            }}
          />
        </Stack>
        <StatusIndicator />
      </View>
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
