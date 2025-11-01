import threading
import queue
import json


class NotificationCenter:
    """Simple in-process notification center (observer pattern).

    - Subscribers get a Queue they can read from (used by the SSE endpoint).
    - Notification messages are JSON strings placed on each subscriber queue.

    Limitations: this is in-memory and process-local (suitable for dev or
    single-process deployments). For production use a centralized broker
    (Redis pub/sub, Kafka, etc) so all processes receive events.
    """

    _lock = threading.Lock()
    _subscribers = []  # list of queue.Queue

    @classmethod
    def subscribe(cls):
        q = queue.Queue()
        with cls._lock:
            cls._subscribers.append(q)
        return q

    @classmethod
    def unsubscribe(cls, q):
        with cls._lock:
            try:
                cls._subscribers.remove(q)
            except ValueError:
                pass

    @classmethod
    def notify(cls, event_type, data):
        payload = json.dumps({"type": event_type, "data": data})
        with cls._lock:
            subs = list(cls._subscribers)
        for q in subs:
            try:
                q.put(payload)
            except Exception:
                # ignore subscriber errors; they may disconnect
                pass
