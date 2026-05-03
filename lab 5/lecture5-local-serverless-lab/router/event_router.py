import os, json, time, redis, requests

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
STREAM_NAME = "events"

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

routes = {
    "image.uploaded": [
        "http://image-resizer:5000/resize",
        "http://notifier:5000/notify"
    ]
}

print("Event Router started. Waiting for events...", flush=True)
last_id = "0-0"

while True:
    try:
        events = r.xread({STREAM_NAME: last_id}, block=5000, count=10)
        if not events:
            continue
        for stream_name, messages in events:
            for message_id, message_data in messages:
                last_id = message_id
                payload = message_data.get("payload")
                if not payload:
                    continue
                event = json.loads(payload)
                event_type = event.get("event_type")
                print(f"Received event: {event_type}", flush=True)
                destinations = routes.get(event_type, [])
                for destination in destinations:
                    try:
                        start = time.time()
                        response = requests.post(destination, json=event, timeout=30)
                        duration_ms = round((time.time() - start) * 1000, 2)
                        print(f"Sent to {destination} | {response.status_code} | {duration_ms}ms", flush=True)
                    except Exception as e:
                        print(f"Error: {e}", flush=True)
    except Exception as main_error:
        print(f"Router error: {main_error}", flush=True)
        time.sleep(3)
