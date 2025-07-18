import pytest
import httpx
import uuid

USERS_URL = "http://localhost:8001/users"
CLIENTS_URL = "http://localhost:8002/clients"
TREES_URL = "http://localhost:8005/inventory"

@pytest.fixture
async def tree_flow():
    email = f"treeflow{uuid.uuid4().hex}@test.com"
    user_data = {
        "email": email,
        "name": "שם בעברית",
        "phone": "0555555555",
        "password": "TreeTestPass1!",
    }
    async with httpx.AsyncClient() as client:
        # הרשמה
        resp = await client.post(f"{USERS_URL}/register", json=user_data)
        assert resp.status_code == 200, resp.text

        # התחברות
        resp = await client.post(f"{USERS_URL}/login", json={"email": email, "password": "TreeTestPass1!"})
        assert resp.status_code == 200, resp.text
        access_token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # יצירת לקוח עם אימייל (הכרחי)
        client_data = {
            "name": "לקוח לעצים",
            "email": f"{uuid.uuid4().hex}@client.com",
            "address": "רחוב הבדיקה 4",
            "phone": "0509999999"
        }
        resp = await client.post(f"{CLIENTS_URL}/", json=client_data, headers=headers)
        assert resp.status_code == 200, resp.text
        client_id = resp.json()["id"]

        yield headers, client_id

@pytest.mark.asyncio
async def test_create_tree_success(tree_flow):
    headers, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Olive",
        "planting_date": "2024-01-01",
        "notes": "טסט עץ רגיל"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        assert resp.status_code == 200, resp.text
        tree = resp.json()
        assert tree["client_id"] == client_id
        assert tree["type"] == "Olive"

@pytest.mark.asyncio
async def test_create_tree_invalid_client_id(tree_flow):
    headers, _ =  tree_flow
    tree_data = {
        "client_id": 987654321,  # לא קיים
        "type": "Orange",
        "planting_date": "2024-04-04",
        "notes": "לא חוקי"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        assert resp.status_code in (403, 404)

@pytest.mark.asyncio
async def test_create_tree_missing_fields(tree_flow):
    headers, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Apple",
        # חסר planting_date
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        assert resp.status_code == 422

@pytest.mark.asyncio
async def test_create_tree_invalid_token(tree_flow):
    _, client_id =  tree_flow
    headers = {"Authorization": "Bearer invalid.token.here"}
    tree_data = {
        "client_id": client_id,
        "type": "Peach",
        "planting_date": "2024-07-01",
        "notes": "טוקן לא תקין"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        assert resp.status_code in (401, 403)

@pytest.mark.asyncio
async def test_get_tree_by_id_success(tree_flow):
    headers, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Fig",
        "planting_date": "2024-08-08",
        "notes": "get by id"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        assert resp.status_code == 200, resp.text
        tree_id = resp.json()["id"]
        # שליפה
        resp = await client.get(f"{TREES_URL}/trees/{tree_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == tree_id

@pytest.mark.asyncio
async def test_get_tree_by_id_not_found(tree_flow):
    headers, _ = tree_flow
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TREES_URL}/trees/99999999", headers=headers)
        assert resp.status_code == 404

@pytest.mark.asyncio
async def test_get_trees_for_client(tree_flow):
    headers, client_id = tree_flow
    async with httpx.AsyncClient() as client:
        for t in ["Olive", "Apple", "Lemon"]:
            tree_data = {
                "client_id": client_id,
                "type": t,  
                "planting_date": "2024-09-09",
                "notes": "בדיקת עץ"
            }
            resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
            assert resp.status_code == 200, f"{resp.status_code} {resp.text}"
        resp = await client.get(f"{TREES_URL}/trees/client/{client_id}", headers=headers)
        assert resp.status_code == 200
        trees = resp.json()
        assert len(trees) >= 3



@pytest.mark.asyncio
async def test_update_tree_success(tree_flow):
    headers, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Olive",
        "planting_date": "2023-11-11",
        "notes": "עדכון"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        tree_id = resp.json()["id"]
        update = {
            "type": "Lemon",
            "planting_date": "2025-12-12",
            "notes": "מעודכן"
        }
        resp = await client.put(f"{TREES_URL}/trees/{tree_id}", json=update, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["type"] == "Lemon"
        assert resp.json()["notes"] == "מעודכן"

@pytest.mark.asyncio
async def test_update_tree_not_found(tree_flow):
    headers, _ = tree_flow
    update = {
        "type": "Banana",
        "planting_date": "2022-01-01",
        "notes": "אין כזה עץ"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"{TREES_URL}/trees/88888888", json=update, headers=headers)
        assert resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_tree_success(tree_flow):
    headers, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Plum",
        "planting_date": "2021-02-02",
        "notes": "מחיקה"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers)
        tree_id = resp.json()["id"]
        resp = await client.delete(f"{TREES_URL}/trees/{tree_id}", headers=headers)
        assert resp.status_code == 200
        resp = await client.get(f"{TREES_URL}/trees/{tree_id}", headers=headers)
        assert resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_tree_not_found(tree_flow):
    headers, _ =  tree_flow
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{TREES_URL}/trees/123456789", headers=headers)
        assert resp.status_code == 404

@pytest.mark.asyncio
async def test_get_trees_empty_list_for_client(tree_flow):
    headers, client_id =  tree_flow
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TREES_URL}/trees/client/{client_id}", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert resp.json() == []

@pytest.mark.asyncio
async def test_tree_action_with_missing_token(tree_flow):
    _, client_id =  tree_flow
    tree_data = {
        "client_id": client_id,
        "type": "Lime",
        "planting_date": "2026-06-06",
        "notes": "אין טוקן"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data)
        assert resp.status_code in (401, 403)

@pytest.mark.asyncio
async def test_tree_get_by_other_user():
    """
    יוצרים עץ עם יוזר אחד ומנסים לשלוף אותו עם יוזר אחר => אמור לקבל 403/404
    """
    email1 = f"user1_{uuid.uuid4().hex}@test.com"
    user1 = {
        "email": email1,
        "name": "משתמש ראשון",
        "phone": "0501234567",
        "password": "Pass123!!"
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{USERS_URL}/register", json=user1)
        resp = await client.post(f"{USERS_URL}/login", json={"email": email1, "password": "Pass123!!"})
        token1 = resp.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        client_data = {
            "name": "לקוח א",
            "email": f"{uuid.uuid4().hex}@client.com",
            "address": "תל אביב",
            "phone": "0502223333"
        }
        resp = await client.post(f"{CLIENTS_URL}/", json=client_data, headers=headers1)
        client_id = resp.json()["id"]

        tree_data = {
            "client_id": client_id,
            "type": "Pine",  # לוודא שזה לפחות 3 תווים, מתאים לרגקס
            "planting_date": "2024-01-01",
            "notes": "בדיקת גישה"
        }
        resp = await client.post(f"{TREES_URL}/trees/", json=tree_data, headers=headers1)
        print("CREATE TREE:", resp.status_code, resp.text)  # תשאיר למעקב עד שהכל ירוץ
        assert resp.status_code == 200, resp.text
        tree_id = resp.json()["id"]

        email2 = f"user2_{uuid.uuid4().hex}@test.com"
        user2 = {
            "email": email2,
            "name": "משתמש שני",
            "phone": "0507654321",
            "password": "Pass123!!"
        }
        await client.post(f"{USERS_URL}/register", json=user2)
        resp = await client.post(f"{USERS_URL}/login", json={"email": email2, "password": "Pass123!!"})
        token2 = resp.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        resp = await client.get(f"{TREES_URL}/trees/{tree_id}", headers=headers2)
        assert resp.status_code in (403, 404)

        resp = await client.delete(f"{TREES_URL}/trees/{tree_id}", headers=headers2)
        assert resp.status_code in (403, 404)
