# OTPTERA

**OTPTERA** is an open-source tool that automates the customized installation and configuration of the [Atera](https://www.atera.com/) remote monitoring and management (RMM) agent. It collects user information during installation and updates the agent's custom fields in the Atera dashboard automatically using their API.

This utility is particularly useful for Managed Service Providers (MSPs) and IT professionals who want to streamline the deployment of Atera agents across client devices with consistent identification and reporting.

---

## 🔗 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Project Relationship](#project-relationship)
- [Disclaimer](#disclaimer)
- [License](#license)

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
