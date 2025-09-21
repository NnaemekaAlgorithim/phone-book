# phone-book

## How to Run as a Desktop App (All Platforms)

### Prerequisites
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux) must be installed.

### Quick Start
1. Copy this folder to your computer (from flash drive or download).
2. Open the folder.
3. **Windows:** Double-click `start.bat`  
	**Mac/Linux:** Run `./start.sh` in a terminal (may need `chmod +x start.sh` first).
4. The app will open in your browser at [http://localhost:8080](http://localhost:8080).

### Stopping the App
- Press `Ctrl+C` in the terminal or command prompt window.

### Notes
- All data is stored in the `postgres_data` Docker volume and persists between runs.
- You can share this folder (with all files) via flash drive or any medium.
- No Python or Django installation is needed on the user's machine—just Docker.

## Running as a Background Service (Daemon)

### Linux (systemd)
1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/phonebook.service
   ```
   Paste the following (update the WorkingDirectory path):
   ```ini
   [Unit]
   Description=Phone Book Docker App
   After=docker.service
   Requires=docker.service

   [Service]
   WorkingDirectory=/absolute/path/to/your/project
   ExecStart=/usr/bin/docker compose up --build
   ExecStop=/usr/bin/docker compose down
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. Reload systemd and enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable phonebook
   sudo systemctl start phonebook
   ```
3. The app will now start at boot and run in the background. Access it at http://localhost:8080

### Windows (Service)
- Use [NSSM (Non-Sucking Service Manager)](https://nssm.cc/) to run `docker-compose up` as a Windows service.
- Or, create a scheduled task to run `start.bat` at login.

### Mac (LaunchAgent/LaunchDaemon)
- Use a LaunchAgent/LaunchDaemon plist to run `docker compose up` at login or boot. See [Apple's documentation](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html) for details.

---

**Note:**
- You can still use the provided scripts for manual start/stop if you prefer.
- For all platforms, Docker Desktop/Engine must be running for the service to work.
