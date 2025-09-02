from flask import Flask, render_template, request, jsonify
import datetime
import os
import webbrowser
import socket
import platform
import wikipedia
import requests
import pandas as pd

app = Flask(__name__)

# --- Skills ---
def rava_greeting(user_input):
    greetings = ["hello", "hi", "hey", "good morning", "good evening"]
    if any(word in user_input for word in greetings):
        return "Hey there 👋 I'm Rava!"
    elif "how are you" in user_input:
        return "I'm running smoothly 😄 How about you?"
    goodbye= ["bye", "see you later", "Goodnight", "good night", "Sweet Dreams"]
    if any(word in user_input for word in goodbye):
        return "Goodbye 👋 Bright trails ✨"
    return None
    
def rava_time(user_input):
    keywords = ["time", "current time", "what time is it", "tell me time", "what's the time", "what is the time"]
    if any(keyword in user_input for keyword in keywords):
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")
    return None
    
def rava_date(user_input):
    date= ["today", "todays date", "Today is on", "When is today", "when is today", "date"]
    if any(keyword in user_input for keyword in date):
        return "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")
    return None

def rava_open_file(user_input):
    triggers = ["open file", "launch file", "start file"]
    if any(t in user_input.lower() for t in triggers):
        filename = user_input
        for t in triggers:
            filename = filename.replace(t, "").strip()

        # Search Desktop recursively
        for root, dirs, files in os.walk("C:/Users/JOHN MWAKIA/Desktop"):
            for f in files:
                if filename.lower() == f.lower():
                    file_path = os.path.join(root, f)
                    os.startfile(file_path)  # 🔹 Opens the file
                    return f"Opening {f}..."
        return "File not found!"
    return None

def rava_search_desktop_db(user_input):
    triggers = ["search db", "open db", "lookup db", "find db"]
    if any(t in user_input.lower() for t in triggers):
        filename = user_input
        for t in triggers:
            filename = filename.replace(t, "").strip()

        for root, dirs, files in os.walk("C:/Users/JOHN MWAKIA/Desktop"):
            for f in files:
                if filename.lower() in f.lower() and f.lower().endswith(('.xlsx', '.xls', '.csv')):
                    file_path = os.path.join(root, f)
                    try:
                        if f.lower().endswith(('.xlsx', '.xls')):
                            df = pd.read_excel(file_path)
                        else:  # CSV
                            df = pd.read_csv(file_path)
                        return f"Found {f}:\n{df.head(5)}"  # show first 5 rows
                    except Exception as e:
                        return f"Could not read the file: {str(e)}"
        return "Database file not found!"
    return None
    
import pyodbc

def rava_access_db(user_input):
    triggers = ["search access", "lookup access"]
    if any(t in user_input.lower() for t in triggers):
        db_path = "C:/Users/JOHN MWAKIA/Desktop/your_database.accdb"
        try:
            conn = pyodbc.connect(
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_path
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Table1")  # replace Table1 with your table
            rows = cursor.fetchall()
            preview = "\n".join([str(row) for row in rows[:5]])  # first 5 rows
            return f"Access DB Preview:\n{preview}"
        except Exception as e:
            return f"Could not read Access DB: {str(e)}"
    return None

def rava_system_info(user_input):
    if "system info" in user_input:
        return f"System: {platform.system()} {platform.release()} | User: {os.getlogin()}"
    return None

def is_online(host="8.8.8.8", port=53, timeout=3):
    """
    Checks internet connection by trying to reach a DNS server (Google).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def rava_play_song(user_input):
    keywords = ["play", "play song", "start song"]
    for keyword in keywords:
        if keyword in user_input.lower():
            song = user_input.lower().replace(keyword, "").strip()
            if not song:
                return "Which song do you want me to play?"

            if is_online():
                # Online → open YouTube
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
                return f"Playing {song} on YouTube 🎵"
            else:
                # Offline → search local playlist folder
                folder = r"C:\Users\JOHN MWAKIA\OneDrive\One Drive\OneDrive\Desktop\mini_rava_web\Music"  # <-- Change to your music folder
                for file in os.listdir(folder):
                    if song.lower() in file.lower():
                        os.startfile(os.path.join(folder, file))
                        return f"Playing {file} from your local playlist 🎵"
                return "Could not find the song locally 😅"
    return None

def rava_google_search(query):
    try:
        # Open Google search in browser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Here’s what I found on Google about '{query}' 🔍"
    except Exception:
        return None

def rava_wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia: {summary}"
    except Exception:
        return None

def rava_fact(user_input):
    # 🔹 Default fact lookup chain
    wiki_result = rava_wikipedia_search(user_input)
    if wiki_result:
        return wiki_result
        
    google_result = rava_google_search(user_input)
    if google_result:
        return google_result

    

    return "Sorry, I couldn’t find any info on that."
    

def rava_response(user_input):
    user_input = user_input.lower()

    # 1️⃣ Check greeting / basic commands first
    for func in [rava_greeting, rava_time, rava_date, rava_open_file, rava_play_song, is_online, rava_fact, rava_google_search, rava_wikipedia_search, rava_access_db, rava_access_db, rava_search_desktop_db]:
        result = func(user_input)
        if result:
            return result

    # 2️⃣ Default: Wikipedia search
    wiki_result = rava_wikipedia_search(user_input)
    if wiki_result:
        return wiki_result

    # 3️⃣ Optional fallback: Google / SerpApi
    google_result = rava_google_search(user_input)
    if google_result:
        return google_result

    # 4️⃣ Still nothing? Generic fallback
    return "Hmm 🤔 I’m still learning. Try another command."

# --- Flask routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print("Received message:", user_message)
    reply = rava_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)