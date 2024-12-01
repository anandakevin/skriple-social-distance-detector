import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

SCRIPT_TO_RUN = "controllers/sd_controller.py"

class RestartHandler(FileSystemEventHandler):
    def __init__(self, process_runner):
        self.process_runner = process_runner

    def on_any_event(self, event):
        # Exclude changes to the watcher script itself
        if event.src_path.endswith(".py") and not event.src_path.endswith("watch_script.py"):
            print(f"Detected change in: {event.src_path}")
            self.process_runner.restart_process()

class ProcessRunner:
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run
        self.process = None

    def start_process(self):
        print(f"Starting process: {self.script_to_run}")
        try:
            self.process = subprocess.Popen(
                ["python", self.script_to_run],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            # Log server output for troubleshooting
            for line in self.process.stdout:
                print(line.decode(), end="")
        except Exception as e:
            print(f"Error starting process: {e}")
            self.process = None

    def restart_process(self):
        if self.process:
            print("Stopping current process...")
            self.stop_process()
        print("Restarting process...")
        self.start_process()

    def stop_process(self):
        if self.process:
            try:
                if os.name == "nt":  # Windows
                    self.process.terminate()
                else:  # Unix-like systems
                    self.process.send_signal(subprocess.signal.SIGINT)
                self.process.wait()
            except Exception as e:
                print(f"Error stopping process: {e}")
            finally:
                self.process = None

if __name__ == "__main__":
    # Set up the process runner
    runner = ProcessRunner(SCRIPT_TO_RUN)
    runner.start_process()

    # Set up the file watcher
    event_handler = RestartHandler(runner)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Stopping watcher...")
        observer.stop()
        runner.stop_process()

    observer.join()
