# Event Management System with QR Code Verification

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

A comprehensive event management system that handles participant registration, QR code generation, and real-time verification using webcam scanning.

## Features

- **Participant Registration**
  - Register participants with name and phone number
  - Automatic unique ID generation
  - QR code generation for each participant
  - WhatsApp notification with QR code

- **QR Code Verification**
  - Live webcam scanning
  - Database lookup for verification
  - Real-time verification feedback
  - Mobile-friendly scanning interface

- **Participant Management**
  - View all registered participants
  - Search and filter functionality
  - Export participant data

- **Security Features**
  - Unique ID verification
  - QR code expiration (optional)
  - Secure database storage

## Tech Stack

- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **QR Generation**: qrcode[pil]
- **WhatsApp Integration**: pywhatkit
- **QR Scanning**: jsQR

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/event-management-system.git
   cd event-management-system
