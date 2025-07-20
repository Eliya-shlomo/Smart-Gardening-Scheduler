
// Base addresses for each microservice
// You need to have the IP address of your computer.You need to have the IP address of your computer.
const LOCALHOST = "http://<your-local-ip>";

// User Service - Registration, Login, Profile
export const BASE_URL_USERS = `${LOCALHOST}:8001`;

// Customer Service - Create a customer, customer list
export const BASE_URL_CLIENTS = `${LOCALHOST}:8002`;

// Log service - personal or system logs
export const BASE_URL_AUDIT = `${LOCALHOST}:8003`;

// Appointment service - appointment scheduling
export const BASE_URL_APPOINTMENTS = `${LOCALHOST}:8004`;

// Inventory Service - Equipment Management
export const BASE_URL_INVENTORY = `${LOCALHOST}:8005`;

// Additional queue service (if there is a split)
export const BASE_URL_APPOINTMENTS_2 = `${LOCALHOST}:8006`;

// Notification service - sending reminders, emails, etc.
export const BASE_URL_NOTIFICATION = `${LOCALHOST}:8007`;
