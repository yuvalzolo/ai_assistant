# tests/test_chat_flow.py


def test_full_flow(client, mocker):
    """
    Happy-path: create assistant → start chat → send message → get mocked reply.
    """
    # 1️⃣ stub Gemini so we don't burn quota
    mocker.patch("app.services.run_chat", return_value="Mocked reply")

    # 2️⃣ create assistant
    resp = client.post(
        "/assistants",
        json={"name": "TestChef", "system_prompt": "Be concise."},
    )
    assert resp.status_code == 201
    assistant_id = resp.json()["id"]

    # 3️⃣ start chat
    resp = client.post("/chats", json={"assistant_id": assistant_id})
    assert resp.status_code == 201
    chat_id = resp.json()["id"]

    # 4️⃣ send message
    resp = client.post(
        f"/chats/{chat_id}/messages",
        json={"content": "Hello!"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "assistant"
    assert data["content"] == "Mocked reply"
