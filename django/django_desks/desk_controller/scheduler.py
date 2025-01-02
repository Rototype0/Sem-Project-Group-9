import threading
import time
from .views import fetch_and_update_desks

def start_scheduler():
    def fetch_task():
        while True:
            try:
                print("Fetching and updating desks...")
                fetch_and_update_desks()
            except Exception as e:
                print(f"Error in scheduled task: {e}")
            time.sleep(5)

    thread = threading.Thread(target=fetch_task, daemon=True)
    thread.start()
