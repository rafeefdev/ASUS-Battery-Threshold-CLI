# ASUS Battery Threshold CLI

A simple and lightweight command-line tool written in Python to help ASUS laptop users manage battery charge thresholds on Ubuntu using **TLP**.

---

## 🧬 Why Use This?

Laptop batteries degrade faster when constantly charged to 100%. This tool allows you to:

- ✅ Limit charge to 80% to preserve battery health
- 🔋 Restore full 100% charge mode when needed
- 🛡️ Automatically backup your TLP configuration
- 📜 Log all operations for transparency and troubleshooting

---

## 📏 Features

- CLI with simple English UI
- Spinner animation on dependency checks
- Dependency validation
- Error-handling with clear messages
- Threshold validation (0–100%)
- Safe file backup and edit
- Logs every operation

---

## 🔧 Requirements

- Linux (tested on Ubuntu-based distros)
- Python 3.x
- [`TLP`](https://linrunner.de/tlp/)
- ASUS laptop with `asus_wmi` kernel module support

---

## 🛠️ Installation and Usage

### 1. Install TLP if not already installed

```bash
sudo apt update
sudo apt install tlp
```

### 2. Clone this repository

```bash
git clone https://github.com/your-username/asus-battery-threshold-cli.git
cd asus-battery-threshold-cli
```

### 3. Run the script with root privileges

```bash
sudo python3 battery_threshold_cli.py
```

> ⚠️ Must be run with `sudo` to modify `/etc/tlp.conf`.

---

## 🔐 Security Notes

- Creates a timestamped backup of your `/etc/tlp.conf` before applying changes.
- Logs all actions to `~/.battery_threshold_cli.log`.
- Input is validated to prevent misconfiguration.

---

## 📁 Log & Backup Files

- `~/.battery_threshold_cli.log` – Operation logs
- `/etc/tlp.conf.bak.YYYYMMDD_HHMMSS` – Auto-backup before every config change

---

## 🔄 Example Run

```bash
=== Dependency Check ===
[✓] TLP is installed.
[✓] Current threshold setting found: 80%

=== ASUS Battery Charging Threshold CLI ===
1. Set charging limit to 80% (Preserve battery health)
2. Set charging limit to 100% (Full charge)
3. Exit
Select an option [1-3]:
```

---

## 📅 Roadmap & Ideas

- [ ] Multi-battery support (BAT1)
- [ ] GUI with Tkinter or TUI with `curses`
- [ ] Automatic detection of optimal threshold based on usage pattern
- [ ] Threshold toggle without restarting TLP

---

## 🙌 Contributing

Feel free to open issues, fork the repo, and send PRs!

---

## 📄 License

MIT License – do anything, but at your own risk 😉

---

## 👤 Author

Made with ❤️ by [Your Name]  
[GitHub](https://github.com/your-username)

