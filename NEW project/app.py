from flask import Flask, render_template, request, jsonify
import math
import webbrowser
import threading
import os

app = Flask(__name__)

# ist
HISTORY_FILE = "history.txt"
if not os.path.exists(HISTORY_FILE):
    open(HISTORY_FILE, "w").close()

def save_history(entry: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def load_history():
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# funk
allowed_names = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}
allowed_names.update({
    "abs": abs,
    "round": round,
    "pow": pow,
    "pi": math.pi,
    "e": math.e
})

@app.route("/")
def index():
    return render_template("index.html", history=load_history())

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expr = data.get("expression", "").replace("^", "**")
    try:
        result = eval(expr, {"__builtins__": None}, allowed_names)
        entry = f"{expr.replace('**','^')} = {result}"
        save_history(entry)
        return jsonify(success=True, result=result, entry=entry)
    except ZeroDivisionError:
        return jsonify(success=False, error="Division by zero.")
    except SyntaxError:
        return jsonify(success=False, error="Invalid syntax.")
    except NameError:
        return jsonify(success=False, error="Disallowed symbols.")
    except Exception as e:
        return jsonify(success=False, error=str(e))

def open_browser():
    webbrowser.open_new("http://126.0.0.1:8080/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="126.0.0.1", port=8080, debug=False)
