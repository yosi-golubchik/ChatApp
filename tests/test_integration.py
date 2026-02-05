import pytest
import uuid
import time
import httpx
from src.redis import get_redis_client

# Define the base URL of your API
BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def redis_client():
    """Provides a Redis client for the tests"""
    return get_redis_client()


def test_full_flow(redis_client):
    """
    Sends a message via API and verifies it appears in Redis.
    Requires: Docker + Worker running!
    """
    # 1. Setup: Generate a unique room ID so tests don't clash
    unique_room_id = f"test_room_{uuid.uuid4().hex[:8]}"
    sender = "pytest_user"
    content = f"Hello from test {unique_room_id}"

    # 2. Action: Send the message via HTTP
    payload = {
        "sender_id": sender,
        "room_id": unique_room_id,
        "content": content
    }

    response = httpx.post(f"{BASE_URL}/send_message", json=payload)
    assert response.status_code == 200, "API did not accept the message"

    # 3. Verification: Poll Redis until the data appears
    # (The worker might take 100ms - 2000ms to process it)
    stream_key = f"room_history:{unique_room_id}"
    found = False

    # Try 10 times, waiting 0.5s each time (Max 5 seconds wait)
    for _ in range(10):
        # xlen checks how many messages are in the stream
        if redis_client.exists(stream_key) and redis_client.xlen(stream_key) > 0:
            found = True
            break
        time.sleep(0.5)

    assert found, "Worker failed to save message to Redis within 5 seconds"

    # 4. Deep Verification: Check the content
    # xrange returns a list of items: [(message_id, {data})]
    messages = redis_client.xrange(stream_key)
    last_message = messages[-1]  # Get the last one
    message_data = last_message[1]  # The dictionary inside

    # Redis stores data as strings, but depending on client config, verify it matches
    assert message_data['user'] == sender
    assert message_data['msg'] == content

    print(f"\nTest Passed! Room: {unique_room_id}")