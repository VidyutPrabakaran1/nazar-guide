# Nazar Guide 🗺️ [DEMO] 

Live Demo Video - https://drive.google.com/file/d/1Axp7oi130KuddD5rRRAkFtHwxcMD_R7-/view?usp=sharing
Code Explanation Video - https://drive.google.com/file/d/1wYcUbadw2s-X3jQaTG3MZeLxw95amC-t/view?usp=sharing

To try this out without actually being in the demo area, you can just shake your phone with the sensor logger app, to simulate steps.

Nazar Guide [DEMO] is a voice based program with the intention to help blind people to traverse the world. In this demo it is only equipped with a singular route in suburban India. 

## Setup [ This demo has only been tested for Windows 10/11 ]

### 1) Install Ollama
 - Get the Ollama installer from [here](https://ollama.com/download), and go through the installer steps.
 - Once installed, open a new command prompt window, and type the following to install the Gemma 3 (1B) model:

   `ollama pull gemma3:1b`

### 2) Install Python 3.12 (PyAudio Library doesn't work on version >3.12)
 - Download Python version 3.12.2 installer from [here](https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe), and go through the installer steps.

### 3) Install required python libraries
 - Open a new command prompt windows, and type the following to install the required python libraries:

   `pip install ollama requests SpeechRecognition pyttsx3 flask PyAudio`

### 4) Setup Sensor Logger on your Android/iOS Phone
 - Install the app on Android - [Google Playstore](https://play.google.com/store/apps/details?id=com.kelvin.sensorapp)
 - Install the app on iOS - [Apple App Store](https://apps.apple.com/us/app/sensor-logger/id1531582925)

 - Once installed, follow these steps:
  -  (1) Enable the Pedometer sensor and click 'Allow' on required permissions when prompted.
  -  (2) Open settings.
  -  (3) Click on Data Streaming
  -  (4) Enable HTTP Push & click on 'Push URL'
    <img width="1920" height="1080" alt="wrwgrsr" src="https://github.com/user-attachments/assets/ffdbbf2d-2b78-4cc3-87fa-34473fae14e1" />

### 5) The Main Program
 - Clone this repository or go to the releases tab and download the nazar_guide.zip file and extract it.
 - Run the file `main.py`
 - Once you get to the output where there are 2 http addresses, copy the second one and type out the same on the Sensor Logger app on your phone.
 - <img width="1920" height="1080" alt="cxc" src="https://github.com/user-attachments/assets/dc1959b5-0ef9-42a5-87a6-9783e2f8bd7f" />
 - The program is now fully setup! Press 'Start Recording' on the app on your phone, and start walking to receive directions.

## Credits
 Made by Vidyut Prabakaran ( [Website](https://vidyutprabakaran.github.io/) ) & Muhammad Zaid Landge ( [YouTube - Zapped Zaid](https://www.youtube.com/@ZappedZaid5) )
