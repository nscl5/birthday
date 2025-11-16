from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
OWNER = "Arshia"

MESSAGES = {
    "fatemeh": {
        "name": "Fatemeh",
        "message": """Happy Birthday, Fatemeh! 🥳
        
It's been so great getting to know you in our class. You're a wonderful friend. 
I hope you have an amazing day and a fantastic year ahead, full of happiness, health, and success!
        
Best wishes,
— Arshia"""
    },
    "mohammad_hassan": {
        "name": "Mohammad Hassan",
        "message": """Happy Birthday, Mohammad Hassan! 🎉
        
Man, it's been fun having you in class all this time. You're a great guy! 
Wishing you a very happy birthday and an awesome year. Hope it's filled with good times and new achievements.
        
Cheers,
— Arshia"""
    }
}

LOGIN_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A Message For You</title>
  <style>
    body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial;display:flex;min-height:100vh;align-items:center;justify-content:center;background:linear-gradient(45deg, #FFDDE1, #FFEFBA);color:#333333;margin:0}
    .card{width:92%;max-width:720px;background:rgba(255, 255, 255, 0.8);padding:28px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,0.1); animation: fadeIn 0.5s ease-out; backdrop-filter: blur(10px);}
    h1{margin:0 0 8px;font-size:22px; color: #8E44AD;}
    p{margin:6px 0 14px;line-height:1.45}
    label{display:block;margin-top:8px;font-size:13px;color:#555;}
    input[type=text]{width:100%;padding:10px;border-radius:8px;border:1px solid #ddd;background:#fff;color:#333;box-sizing: border-box;}
    .btn{display:inline-block;margin-top:12px;padding:10px 14px;border-radius:10px;border:0;background:#8E44AD;color:white;cursor:pointer;font-size:15px;text-decoration:none;transition: background-color 0.2s;}
    .btn:hover{background:#6C3483}
    .error{color:#E74C3C;margin-top:10px;font-size:14px;}
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  </style>
</head>
<body>
  <div class="card">
    <h1>Hello 👋</h1>
    <p>This is a small birthday surprise prepared by {{ owner }}. Please enter your first-name to continue.</p>
    <form method="post" action="/greet">
      <label for="name">Your name:</label>
      <input id="name" name="name" type="text" autocomplete="off" required>
      <button class="btn" type="submit">Open</button>
    </form>
    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

GREET_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Happy Birthday!</title>
<style>
  body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial;background:linear-gradient(45deg, #FFDDE1, #FFEFBA);color:#333333;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
  .box{width:94%;max-width:820px;padding:28px;border-radius:12px;background:rgba(255, 255, 255, 0.8);box-shadow:0 14px 40px rgba(0,0,0,0.1); animation: fadeIn 0.5s ease-out; backdrop-filter: blur(10px);}
  h2{margin:0 0 8px; font-size: 24px; color: #8E44AD;}
  p{margin:6px 0 12px; line-height: 1.6;}
  .message-block{white-space:pre-wrap;font-family:monospace;background:rgba(0,0,0,0.05);padding:16px;border-radius:8px; font-size: 15px; line-height: 1.7; color: #333;}
  .cake-area{text-align:center; margin: 20px 0 15px;}
  .cake{font-size: 6rem;}
  .candles{font-size: 3rem; letter-spacing: 5px; margin-top: -20px;}
  .action{margin-top:20px}
  .btn{display:inline-block; padding:10px 14px;border-radius:10px;border:0;background:#8E44AD;color:white;cursor:pointer;font-size:15px;text-decoration:none;transition: background-color 0.2s;}
  .btn:hover{background:#6C3483;}
  @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
</head>
<body>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const message = `{{ message }}`;
      const messageBlock = document.getElementById('message-block');
      let i = 0;
      function typeWriter() {
        if (i < message.length) {
          messageBlock.innerHTML += message.charAt(i);
          i++;
          setTimeout(typeWriter, 50);
        }
      }
      typeWriter();
    });
  </script>
  <div class="box">
    <h2>Happy Birthday, {{ name }}!</h2>
    <p>A small message from {{ owner }}:</p>
    <div id="message-block" class="message-block"></div>
    
    <div class="cake-area">
      <div class="candles">🕯️🕯️🕯️</div>
      <div class="cake">🎂</div>
    </div>
    
    <div class="action">
      <a href="{{ url_for('finale', name=name) }}" class="btn">Make a wish and blow out the candles!</a>
    </div>
  </div>
</body>
</html>
"""

FINAL_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wishes!</title>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<style>
  body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial;background:linear-gradient(45deg, #FFDDE1, #FFEFBA);color:#333333;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0; text-align:center;}
  .wrap{width:94%;max-width:820px;padding:28px;border-radius:12px;background:rgba(255, 255, 255, 0.8);box-shadow:0 12px 36px rgba(0,0,0,0.1); animation: fadeIn 0.5s ease-out; backdrop-filter: blur(10px);}
  h1{margin:0 0 6px; font-size: 30px; color: #8E44AD;}
  p{margin:6px 0 12px; font-size: 18px;}
  .cake{font-size: 6rem; margin-top: 10px;}
  @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
</head>
<body>
  <div class="wrap">
    <h1>Woooo! Happy Birthday, {{ name }}! 🎉</h1>
    <p>All the best wishes from {{ owner }}.</p>
    <div class="cake">🎂</div>
  </div>
  
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      confetti({
        particleCount: 150,
        spread: 100,
        origin: { y: 0 }
      });
      setTimeout(function() {
        confetti({
          particleCount: 100,
          spread: 120,
          origin: { x: 0.5, y: 0.6 }
        });
      }, 400);
    });
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    """Shows the login page."""
    error = request.args.get('error')
    return render_template_string(LOGIN_HTML, owner=OWNER, error=error)

@app.route('/greet', methods=['POST'])
def greet():
    """Handles the name check and shows the greeting page."""
    name = (request.form.get('name') or '').strip()
    normalized_name = name.lower()

    person_key = None

    if normalized_name in ['fatemeh', 'فاطمه']:
        person_key = 'fatemeh'
    elif normalized_name in ['mohammad hassan', 'محمد حسن']:
        person_key = 'mohammad_hassan'
        
    if person_key:
        person_data = MESSAGES[person_key]
        return render_template_string(
            GREET_HTML, 
            name=person_data['name'], 
            message=person_data['message'], 
            owner=OWNER
        )
    else:
        error_msg = "This page isn't for you 😏🤔"
        return redirect(url_for('index', error=error_msg))

@app.route('/finale')
def finale():
    """Shows the final page with confetti."""
    name = request.args.get('name', 'Friend')
    return render_template_string(FINAL_HTML, name=name, owner=OWNER)

if __name__ == '__main__':
    # This block is for LOCAL TESTING only.
    # PythonAnywhere and Serv00 will IGNORE this.
    app.run(host='0.0.0.0', port=8000, debug=True)
