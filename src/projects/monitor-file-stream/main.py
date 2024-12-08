
# Initialize and start file monitor
monitor = FileMonitor(shutdown_folder="/path/to/shutdown")
monitor.start()

# Start web interface in a separate thread
import threading
web_thread = threading.Thread(
    target=start_web_interface,
    args=(monitor,),
    kwargs={'port': 5000}
)
web_thread.start()