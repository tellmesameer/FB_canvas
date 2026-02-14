import requests
import asyncio
import websockets
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000"

def test_api():
    print("Testing API...")
    
    # 1. Create Room
    slug = f"test-room-{uuid.uuid4()}"
    payload = {
        "room_name": "Integration Test Room",
        "match_duration_minutes": 60,
        "custom_slug": slug
    }
    response = requests.post(f"{BASE_URL}/rooms/", json=payload)
    if response.status_code != 201:
        print(f"Failed to create room: {response.text}")
        return None, None
    
    data = response.json()["data"]
    room_id = data["room_id"]
    print(f"Room created: {room_id} (slug: {slug})")
    
    # Check teams were created
    # Ref: rooms.py creates home/away teams
    # But response might not have them populated if I didn't eager load or refresh correctly in schema
    # Let's fetch teams explicitly
    response_teams = requests.get(f"{BASE_URL}/rooms/{room_id}/teams/")
    if response_teams.status_code != 200:
        print(f"Failed to get teams: {response_teams.text}")
    else:
        teams = response_teams.json()["data"]
        print(f"Teams found: {len(teams)}")
        for team in teams:
            print(f" - {team['name']} ({team['side']})")

    # 2. Start Match
    response_start = requests.post(f"{BASE_URL}/rooms/{room_id}/match/start")
    if response_start.status_code == 200:
        print("Match started successfully.")
    else:
        print(f"Failed to start match: {response_start.text}")

    return room_id, slug

async def test_websocket(room_id):
    print(f"Testing WebSocket for room {room_id}...")
    uri = f"{WS_URL}/ws/{room_id}/test-client-1"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket.")
        
        # Send a test message
        test_msg = {"type": "ping", "content": "hello"}
        await websocket.send(json.dumps(test_msg))
        print(f"Sent: {test_msg}")
        
        # Receive echo (since my simple implementation broadcasts mostly)
        # Note: broadcast excludes sender in my implementation? 
        # "await manager.broadcast(message, room_id, exclude=websocket)"
        # So I won't receive my own message. 
        # I should connect a second client to verify broadcast.
        pass

async def test_websocket_broadcast(room_id):
    print(f"Testing WebSocket Broadcast for room {room_id}...")
    uri1 = f"{WS_URL}/ws/{room_id}/client-1"
    uri2 = f"{WS_URL}/ws/{room_id}/client-2"

    async with websockets.connect(uri1) as ws1, websockets.connect(uri2) as ws2:
        print("Both clients connected.")
        
        msg = {"type": "chat", "text": "Hello from Client 1"}
        await ws1.send(json.dumps(msg))
        print("Client 1 sent message.")
        
        response = await ws2.recv()
        print(f"Client 2 received: {response}")
        
        data = json.loads(response)
        if data == msg:
            print("Verification Successful: Message broadcasted correctly.")
        else:
            print("Verification Failed: Content mismatch.")

if __name__ == "__main__":
    try:
        room_id, slug = test_api()
        if room_id:
            asyncio.run(test_websocket_broadcast(room_id))
    except Exception as e:
        print(f"Verification crashed: {e}")
