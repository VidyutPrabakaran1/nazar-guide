## --- Libraries ---
import ollama
import requests
import speech_recognition as sr 
import pyttsx3
from flask import Flask, request
import subprocess

## --- Misc ---
engine = pyttsx3.init()
engine.setProperty('rate', 160)

app = Flask(__name__)

route_plan = []
current_step_index = 0

init_step_count = None
step_length_m = 0.75

demo_route = [
        {"instruction": "Leave from Silver Park", "trigger_distance": 0},
        {"instruction": "Turn left onto Uday Park Road", "trigger_distance": 53},
        {"instruction": "Turn right", "trigger_distance": 167},
        {"instruction": "Mustard mart is on your right", "trigger_distance": 195}
    ]

## --- Functions ---
def speak(text):
    print(f"\n[AI] Sending to Gemma: {text}")
    
    prompt = f"""Rewrite this navigation instruction for a blind person. 
    Rule 1: Do NOT mention any street or road names.
    Rule 2: Do NOT say 'Okay' or 'Here is a rephrasing'. 
    Rule 3: Output ONLY the physical action.
    Original: {text}
    """

    try:
        response = ollama.chat(model='gemma3:1b', messages=[
            {'role': 'system', 'content': 'You are a strict navigation system. Output only the final instruction. No conversational filler.'},
            {'role': 'user', 'content': prompt}
        ])

        cleaned = response['message']['content'].strip()
        safe_text = cleaned.replace('"', '').replace("'", "")
        print(f"[AI] Gemma says: {safe_text}")
        
        print("[Audio] Spawning isolated audio process...")

        python_code = f"import pyttsx3; engine = pyttsx3.init(); engine.setProperty('rate', 160); engine.say('{safe_text}'); engine.runAndWait()"
        subprocess.run(["python", "-c", python_code])
        
        print("[Audio] TTS finished.")

    except Exception as e:
        print(f"\n[AI Error] Failed to process AI response: {e}")

def speech_to_text():
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source, duration=1)
        engine.say("You can speak now. Please say your destination.")
        engine.runAndWait()

        try:
            audio = recog.listen(source, timeout=5)
            engine.say("Processing what you said... ")
            engine.runAndWait()
            text = recog.recognize_google(audio)
            print(f"\nYou said: {text}\n")
            return text + ""
        except sr.UnknownValueError:
            speak("\nError: Sorry, I could not understand the audio. Please try speaking clearer.")
            return "Sorry, I could not understand the audio. Please try speaking clearer."
        except sr.RequestError as e:
            speak(f"\nError: Could not connect to the internet. Please try again.")
            return "Sorry, I could not connect to the internet. Please try again."
        except sr.WaitTimeoutError:
            speak("\nError: You didn't speak within the 20-second timeout window.")
            return "Sorry, you didn't speak within the 20-second timeout window."
        
def get_directions():
    #print("Loading internal route data...")
    return demo_route
    
@app.route('/data', methods=['POST'])
def sensor_data():
    global current_step_index, init_step_count

    if current_step_index >= len(route_plan):
        return "Arrived", 200

    try:
        data = request.json

        for reading in data.get('payload', []):
            if reading['name'] == 'pedometer':
                current_total_steps = reading['values']['steps']

                if init_step_count is None:
                    init_step_count = current_total_steps
                    print(f"\n[Calibrated] Starting pedometer count at {init_step_count} steps.")

                steps_taken = current_total_steps - init_step_count
                meters_walked = steps_taken * step_length_m

                next_target = route_plan[current_step_index]
                target_distance = next_target['trigger_distance']

                if meters_walked >= target_distance:
                    print(f"\n\n[TRIGGER] Reached waypoint {current_step_index + 1}!")
                    instruction = next_target['instruction']
                    current_step_index += 1
                    
                    speak(instruction) 

    except Exception as e:
        print(f"\n[Flask Error] Failed to process sensor data: {e}")
        pass 
        
    return "OK", 200

## --- Main ---

if __name__ == "__main__":
    a = input("Press enter to start VOICE...")

    # We have disabled voice input for now sicne its not very reliable but it does work in a quiet environment.
    #usr_command = speech_to_text()
    #if "mustard mart" in usr_command.lower():

    if a == "":
        route_plan = get_directions()
        if route_plan:
            startup_engine = pyttsx3.init()
            startup_engine.setProperty('rate', 160)
            startup_engine.say("Navigation loaded. Awaiting Pedometer signal.")
            startup_engine.runAndWait()

            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=False)
        else:
            speak("CRITICAL ERROR: Could not load map data. Shutting down.")
