import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"
# === 0. רישום משתמש חדש ===
register_payload = {
    "name": "nisim",
    "email": "n207302027@gmail.com",
    "phone": "0520000000",
    "password": "StrongPassword123"
}

print("\n=== Register New User ===")
register_response = requests.post(f"{BASE_URL}/users/register", json=register_payload)
print("Status:", register_response.status_code)
print("Response:", register_response.text)

if register_response.status_code == 201 or register_response.status_code == 200:
    print("✅ המשתמש נרשם בהצלחה.")
elif register_response.status_code == 400 and "Email already registered" in register_response.text:
    print("ℹ️ המשתמש כבר קיים – ממשיכים לכניסה.")
else:
    raise Exception("❌ שגיאה ברישום המשתמש – עצירת הטסטים.")



# === 1. התחברות ===
login_payload = {
    "email": "n207302027@gmail.com",
    "password": "StrongPassword123"
}

login_response = requests.post(f"{BASE_URL}/users/login", json=login_payload)
print("\n=== Login ===")
print("Status:", login_response.status_code)
print("Response:", login_response.text)

access_token = login_response.json().get("access_token")
if not access_token:
    raise Exception("❌ התחברות נכשלה – לא התקבל access_token")

auth_headers = {
    "Authorization": f"Bearer {access_token}"
}

# === 2. יצירת לקוח ===
client_payload = {
    "name": "client123",
    "email": "eliyashlomo7@gmail.com",
    "address": "test_address_123",
    "phone": "0521234567"
}

create_response = requests.post(f"{BASE_URL}/clients/", json=client_payload, headers=auth_headers)
print("\n=== Create Client ===")
print("Status:", create_response.status_code)
print("Response:", create_response.text)

try:
    client_id = create_response.json().get("id")
    if not client_id:
        raise ValueError("התגובה לא מכילה מזהה לקוח")
    print(f"✅ לקוח נוצר עם מזהה: {client_id}")
except Exception as e:
    raise Exception(f"❌ יצירת לקוח נכשלה: {e}")

# === 3. בדיקת לקוח לפי מזהה ===
print("\n=== Verify Client Access ===")
client_check = requests.get(f"{BASE_URL}/clients/{client_id}", headers=auth_headers)
print("Status:", client_check.status_code)
print("Response:", client_check.text)
if client_check.status_code != 200:
    raise Exception("❌ לא ניתן לגשת ללקוח לפי מזהה. ייתכן שאינו קיים או שאינו שייך למשתמש.")

# === 4. יצירת עץ ===
tree_payload = {
    "type": "mango",
    "planting_date": datetime.utcnow().isoformat(),
    "notes": "Planted near fence",
    "client_id": client_id
}

print("\n=== Tree Payload ===")
print(tree_payload)

tree_create_response = requests.post(f"{BASE_URL}/trees/", json=tree_payload, headers=auth_headers)
print("\n=== Create Tree ===")
print("Status:", tree_create_response.status_code)
print("Response:", tree_create_response.text)

tree_id = None
try:
    tree_id = tree_create_response.json().get("id")
    if tree_id:
        print(f"✅ עץ נוצר עם מזהה: {tree_id}")
    else:
        print("⚠️ לא הוחזר מזהה עץ – ייתכן שהפעולה נכשלה בשקט.")
except Exception as e:
    print("❌ שגיאה בקריאת תגובת יצירת עץ:", e)

# === 5. שליפת כל העצים של לקוח ===
print("\n=== Get Trees for Client ===")
tree_list_url = f"{BASE_URL}/trees/client/{client_id}"
print("URL:", tree_list_url)
trees_list_response = requests.get(tree_list_url, headers=auth_headers)
print("Status:", trees_list_response.status_code)
print("Response:", trees_list_response.text)

# === 6. שליפת עץ לפי מזהה ===
if tree_id:
    print("\n=== Get Tree by ID ===")
    tree_detail_url = f"{BASE_URL}/trees/{tree_id}"
    print("URL:", tree_detail_url)
    tree_detail_response = requests.get(tree_detail_url, headers=auth_headers)
    print("Status:", tree_detail_response.status_code)
    print("Response:", tree_detail_response.text)
else:
    print("\n⚠️ לא ניתן לשלוף עץ לפי מזהה כי לא התקבל tree_id.")


# === 7. יצירת פגישה ===
appointment_payload = {
    "date": datetime.utcnow().isoformat(),
    "time": "1400",
    "treatment_type": "Haircut",
    "notes": "Short_trim",
    "client_id": client_id
}

print("\n=== Create Appointment ===")
appointment_response = requests.post(f"{BASE_URL}/appointments/", json=appointment_payload, headers=auth_headers)
print("Status:", appointment_response.status_code)
print("Response:", appointment_response.text)

appointment_id = None
try:
    appointment_id = appointment_response.json().get("id")
    if appointment_id:
        print(f"✅ פגישה נוצרה עם מזהה: {appointment_id}")
    else:
        print("⚠️ לא התקבל מזהה פגישה")
except Exception as e:
    print("❌ שגיאה בקריאת תגובת יצירת פגישה:", e)

# === 8. שליפת פגישות לפי מזהה לקוח ===
print("\n=== Get Appointments for Client ===")
appointments_list_response = requests.get(f"{BASE_URL}/appointments/client/{client_id}", headers=auth_headers)
print("Status:", appointments_list_response.status_code)
print("Response:", appointments_list_response.text)
if appointments_list_response.status_code == 200:
    print(f"✅ נמצאו {len(appointments_list_response.json())} פגישות עבור הלקוח")
else:
    print("❌ שליפת פגישות נכשלה")

# === 9. עדכון סטטוס פגישה ל־done ===
if appointment_id:
    print("\n=== Update Appointment Status ===")
    update_payload = {
        "status": "done",
        "notes": "Finished_successfully"
    }
    update_response = requests.patch(f"{BASE_URL}/appointments/{appointment_id}", json=update_payload, headers=auth_headers)
    print("Status:", update_response.status_code)
    print("Response:", update_response.text)

    if update_response.status_code == 200:
        print("✅ סטטוס פגישה עודכן בהצלחה")
    else:
        print("❌ עדכון סטטוס הפגישה נכשל")

# === 10. ניסיון לגשת לפגישה לא קיימת ===
print("\n=== Access Non-existent Appointment ===")
invalid_id = 999999
invalid_response = requests.patch(f"{BASE_URL}/appointments/{invalid_id}", json={"status": "done"}, headers=auth_headers)
print("Status:", invalid_response.status_code)
print("Response:", invalid_response.text)
if invalid_response.status_code == 404:
    print("✅ המערכת החזירה 404 כפי שמצופה לפגישה לא קיימת")
else:
    print("❌ טיפול לא תקין בגישה לפגישה לא קיימת")


# === 11. שליפת המלצות של המשתמש הנוכחי ===
print("\n=== Get Recommendations for Current User ===")
recommendations_response = requests.get(f"{BASE_URL}/recommendations/my", headers=auth_headers)
print("Status:", recommendations_response.status_code)
print("Response:", recommendations_response.text)

if recommendations_response.status_code == 200:
    recommendations = recommendations_response.json()
    print(f"✅ נמצאו {len(recommendations)} המלצות עבור המשתמש")
    if recommendations:
        print("📌 דוגמה להמלצה:")
        print(recommendations[0])
else:
    print("❌ שליפת המלצות נכשלה")