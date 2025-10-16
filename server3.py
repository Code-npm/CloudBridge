from flask import Flask, request, render_template
from flask_socketio import SocketIO
import google.generativeai as genai
import json, time, threading, re 


genai.configure(api_key="AIzaSyBgsjFxO2DR6YJM3y-F9SgJGpvS7qm8eXA")


sensor_data = None


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route("/data", methods=["POST"])
def send_live_data():
    global sensor_data

    sensor_data = request.get_json()
    data = sensor_data
    print(data)
    socketio.emit("sensor_data",data)

    return "recieved"  

@app.route('/')
def index():
    return render_template('index.html')

def send_result():
    global sensor_data
    while True:
        
        results = result()
        print(results)
        try:
            socketio.emit("result_text", json.loads(results))
        except Exception as e:
            print("Error:", e)
        time.sleep(50)
        
        
def result():
    prompt = f"""
        You are a food-quality expert.
        below is the environmental data (temperature, humidity, and gas readings) from a refrigerator.
        
        Analyze the data and determine:
        1. Whether items are fresh, spoiled, or about to spoil, like something is spoiled ,everythig is fresh,
        2. Give a very short reason for your judgment  

        Sensor data:
        {json.dumps(sensor_data, indent=2)}
        
        Respond strictly in JSON format like this:
        {{
          "status": "fresh" or "spoiled" or "about to spoil",
          "reason": "very short human-like explanation"
        }}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    text = response.text.strip()
    ans = re.search(r'\{.*\}', text, re.DOTALL)
    
    if ans:
        answer = ans.group(0)
    else:
        answer = json.dumps({
            "status": "unknown",
            "reason": "Could not parse model response"
        })

    return answer

if __name__ == "__main__":
    
    threading.Thread(target=send_result, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5555,debug=True, use_reloader=False,allow_unsafe_werkzeug=True)





