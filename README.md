
# Classtractor

**Classtractor** is a Python tool designed to automate the extraction and testing of Android activities from APK files. It simplifies Android application analysis by identifying accessible activities that may bypass security controls, helping cybersecurity engineers uncover potential misconfigurations.

## Features

- **Automated Activity Extraction**: Extracts Android activities using the Android Asset Packaging Tool (aapt).
- **Systematic Activity Testing**: Tests each extracted activity using the Activity Manager (am) through ADB.
- **Security Misconfiguration Detection**: Helps identify accessible activities behind security controls, revealing potential vulnerabilities.

## Requirements

- Python +3.7
- ADB (Android Debug Bridge) installed
- aapt (Android Asset Packaging Tool) installed

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/D4rkTT/Classtractor
   cd classtractor
   ```

## Usage

1. Connect your Android device or emulator via ADB
2. Install required APK.
3. Run Classtractor:

   ```bash
   python classtractor.py
   ```
4. Enter APK, AAPT, ADB files path

## License

This project is licensed under the Apache-2.0 license.
