import threading
import time
from .views import fetch_all_desk_states

def start_scheduler():
    def fetch_task():
        while True:
            try:
                print("Fetching and updating desks...")
                fetch_all_desk_states()
            except Exception as e:
                print(f"Error in scheduled task: {e}")
            time.sleep(60)

    thread = threading.Thread(target=fetch_task, daemon=True)
    thread.start()
