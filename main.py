import os
import sys
import shutil
import time
import threading
import subprocess
import logging
from datetime import datetime

TLP_CONF_PATH = "/etc/tlp.conf"
BACKUP_PATH = "/etc/tlp.conf.bak"
LOG_PATH = os.path.expanduser("~/.battery_threshold_cli.log")

# === Logging Setup ===
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Spinner Animation ===
spinner_running = True

def spinner(message):
    global spinner_running
    chars = ['|', '/', '-', '\\']
    i = 0
    while spinner_running:
        sys.stdout.write(f"\r{message}... {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

# === Check if TLP is installed ===
def check_tlp_installed():
    global spinner_running
    spinner_running = True
    t = threading.Thread(target=spinner, args=("Checking if TLP is installed",))
    t.start()
    try:
        time.sleep(1.5)
        if shutil.which("tlp") is None:
            raise FileNotFoundError("TLP not found")
        print("\n[✓] TLP is installed.")
    except FileNotFoundError:
        print("\n[✗] TLP is not installed. Please install it using:")
        print("    sudo apt install tlp")
        logging.error("TLP not installed.")
        sys.exit(1)
    finally:
        spinner_running = False
        t.join()

# === Check if threshold is already set ===
def check_threshold_set():
    try:
        with open(TLP_CONF_PATH, 'r') as file:
            lines = file.readlines()
        for line in lines:
            if line.strip().startswith("STOP_CHARGE_THRESH_BAT0"):
                value = line.strip().split("=")[-1].strip()
                print(f"[✓] Current threshold setting found: {value}%")
                return value
        print("[!] Threshold setting not found in configuration file.")
        return None
    except FileNotFoundError:
        print(f"[!] File not found: {TLP_CONF_PATH}")
        logging.error("Configuration file not found.")
        sys.exit(1)
    except PermissionError:
        print("[!] Permission denied. Please run as root.")
        logging.error("Permission denied while reading configuration file.")
        sys.exit(1)

# === Update the threshold setting ===
def update_threshold(value):
    if not isinstance(value, int) or not 0 <= value <= 100:
        print("[!] Threshold value must be an integer between 0 and 100.")
        logging.warning("Invalid threshold value attempted: %s", str(value))
        return

    try:
        # Backup original config with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(TLP_CONF_PATH, f"{BACKUP_PATH}.{timestamp}")

        with open(TLP_CONF_PATH, 'r') as file:
            lines = file.readlines()

        lines = [line for line in lines if not line.strip().startswith("STOP_CHARGE_THRESH_BAT0")]
        lines.append(f"\nSTOP_CHARGE_THRESH_BAT0={value}\n")

        with open(TLP_CONF_PATH, 'w') as file:
            file.writelines(lines)

        print(f"[✓] Charging threshold set to {value}%")
        logging.info("Threshold set to %d", value)

        result = subprocess.run(["tlp", "start"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[✓] TLP restarted successfully")
            logging.info("TLP restarted successfully")
        else:
            print("[!] Failed to restart TLP: " + result.stderr)
            logging.error("Failed to restart TLP: %s", result.stderr)

    except PermissionError:
        print("[!] Please run this script as root using sudo.")
        logging.error("Permission denied while updating configuration file.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        logging.exception("Exception occurred")
        sys.exit(1)

# === Main Menu ===
def main():
    if os.geteuid() != 0:
        print("[!] You must run this script as root. Try: sudo python3 battery_threshold_cli.py")
        sys.exit(1)

    print("=== Dependency Check ===")
    check_tlp_installed()
    check_threshold_set()

    while True:
        print("\n=== ASUS Battery Charging Threshold CLI ===")
        print("1. Set charging limit to 80% (Preserve battery health)")
        print("2. Set charging limit to 100% (Full charge)")
        print("3. Exit")

        try:
            choice = input("Select an option [1-3]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Exiting...")
            break

        if choice == '1':
            update_threshold(80)
        elif choice == '2':
            update_threshold(100)
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
