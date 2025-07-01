# OTPTERA

**OTPTERA** is an open-source tool that automates the customized installation and configuration of the [Atera](https://www.atera.com/) remote monitoring and management (RMM) agent. It collects user information during installation and updates the agent's custom fields in the Atera dashboard automatically using their API.

This utility is particularly useful for Managed Service Providers (MSPs) and IT professionals who want to streamline the deployment of Atera agents across client devices with consistent identification and reporting.

---

## 🔗 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Requirements](#-requirements)
- [Configuration](#-configuration)
- [Project Relationship](#-project-relationship)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 📌 About the Project

**OTPTERA** simplifies the installation of Atera’s agent by packaging the process into a self-contained executable. Upon execution, it:

- Installs the Atera agent silently.
- Prompts the user for key contact details (full name, email, phone).
- Detects the device’s serial number and network information.
- Uses the Atera public API to:
  - Find the newly installed agent.
  - Update custom fields with the collected user data.
- Sends an email confirmation report for each installation attempt.

This makes it easier for technicians to identify devices and users directly from the Atera console, without manual input.

---

## ✨ Features

- ✅ Silent installation of Atera agent via MSI.
- ✅ User prompts for contact information at install time.
- ✅ Serial number detection (via PowerShell).
- ✅ Public IP and hostname detection.
- ✅ Agent field update via Atera API (custom fields).
- ✅ Email reporting of success/failure (SMTP).
- ✅ Logging to local file.

---

## ⚙️ How It Works

The script performs the following steps:

1. **Checks for Admin Privileges**  
   Required to install software and access system info.

2. **Prompts for User Information**  
   Inputs include full name, email, and contact phone.

3. **Downloads and Installs the Atera Agent**  
   Uses a hardcoded installer URL, if not already installed.

4. **Fetches Device Metadata**  
   Gathers serial number and network details (host/IPs).

5. **Searches for the Agent via API**  
   Matches agent in Atera using serial number.

6. **Updates Custom Fields**  
   Updates “User Name”, “Email”, “Phone”, and “Install Date”.

7. **Sends Confirmation via Email**  
   Sends device and user info to a predefined inbox.

---

## 🛠 Installation

> You can compile the script into an `.exe` using [PyInstaller](https://pyinstaller.org/) to deploy it more easily.

1. Clone the repository:
   ```bash
   git clone https://github.com/aromeuemtc/otptera.git
   cd otptera
   ```

2. Install dependencies (if needed):
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script (as administrator):
   ```bash
   python atera_installer.py
   ```

To compile into `.exe`:
```bash
pyinstaller --onefile atera_installer.py
```

---

## 📋 Requirements

- OS: Windows (with admin privileges)
- Python 3.x
- Internet connection
- A valid [Atera API Key](https://support.atera.com/hc/en-us/articles/360012537919)
- SMTP credentials (for report emails)

---

## 🔗 Project Relationship

This project is maintained by Alvaro Romeu Esquerre [@aromeuemtc](https://github.com/aromeuemtc), and is used internally to support automated agent deployment in some environments.

The project is open-source and available to the public under the MIT license. Third parties are welcome to fork, adapt, or contribute.

---

## ⚠️ Disclaimer

**OTPTERA** is not affiliated with or endorsed by Atera Networks Ltd.  
It uses their public API according to their documented usage guidelines.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
