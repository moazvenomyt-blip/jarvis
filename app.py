import os
import secrets
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "MNUBQXVM4SBzrA4AbVeB")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#050b14"><title>JARVIS AI</title>
<style>
:root{--bg:#050b14;--panel:rgba(9,24,40,.78);--line:rgba(46,190,255,.25);--cyan:#39d7ff;--blue:#168bff;--muted:#8ba8bd}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% 25%,#102c46 0,#071321 38%,#03070d 100%);color:#eaf8ff;font:15px system-ui,Segoe UI,sans-serif;min-height:100vh}
header{display:flex;justify-content:space-between;align-items:center;padding:18px 5%;border-bottom:1px solid var(--line);background:#06101dcc;position:sticky;top:0;backdrop-filter:blur(16px);z-index:3}
.brand{letter-spacing:.22em;font-weight:800;color:var(--cyan)}.status{font-size:12px;color:#8ee9ff}
main{max-width:1100px;margin:auto;padding:24px 18px 60px}.top{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:center}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 0 32px #008cff12;backdrop-filter:blur(12px)}
.corebox{display:grid;place-items:center;min-height:330px}.core{width:205px;height:205px;border-radius:50%;border:1px solid #55dcff;box-shadow:0 0 18px #13bfff, inset 0 0 35px #008cff55;display:grid;place-items:center;position:relative;background:radial-gradient(circle,#164d70 0,#071a2b 56%,#06101a 70%)}
.core:before,.core:after{content:"";position:absolute;inset:-15px;border:1px solid #25bfff88;border-radius:50%;animation:spin 12s linear infinite}.core:after{inset:-29px;border-color:#168bff55;border-style:dashed;animation-direction:reverse;animation-duration:20s}
.core span{font-size:25px;letter-spacing:.18em;color:#baf4ff;text-shadow:0 0 18px var(--cyan)}@keyframes spin{to{transform:rotate(360deg)}}
h1{font-size:clamp(27px,5vw,44px);margin:0 0 8px;letter-spacing:.08em}h2{font-size:17px;color:var(--cyan);letter-spacing:.12em;margin:0 0 14px}.muted{color:var(--muted);line-height:1.6}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}.metric{padding:12px;border:1px solid var(--line);border-radius:12px;text-align:center}.metric b{display:block;color:var(--cyan);font-size:18px}
.chat{margin-top:20px}.messages{height:280px;overflow:auto;padding:12px;background:#030a12;border:1px solid var(--line);border-radius:12px;display:flex;flex-direction:column;gap:12px}.msg{max-width:90%;padding:11px 14px;border-radius:12px;line-height:1.5;white-space:pre-wrap}.bot{align-self:flex-start;background:#0d2940;border:1px solid #1b6387}.user{align-self:flex-end;background:#123d61;border:1px solid #268bc4}
.controls{display:flex;gap:9px;margin-top:12px}.controls input{min-width:0;flex:1}.field{background:#071522;color:white;border:1px solid var(--line);border-radius:10px;padding:13px;font:inherit;outline:none}.btn{background:linear-gradient(120deg,#087bc4,#13bfe8);color:#00121d;border:0;border-radius:10px;padding:12px 16px;font-weight:800;cursor:pointer}.btn.secondary{background:#10283b;color:#c9f5ff;border:1px solid var(--line)}.btn:disabled{opacity:.5}
.tools{display:flex;flex-wrap:wrap;gap:9px;margin-top:15px}.tools a{color:#a9edff;text-decoration:none;border:1px solid var(--line);padding:10px 13px;border-radius:10px;background:#0a1b2a}
footer{text-align:center;color:#69869b;font-size:12px;padding:25px}
@media(max-width:720px){.top{grid-template-columns:1fr}.corebox{min-height:270px}.core{width:165px;height:165px}.controls{flex-wrap:wrap}.controls input{flex-basis:100%}.metrics{grid-template-columns:repeat(3,1fr)}}
</style></head>
<body>
<header><div class="brand">JARVIS <span style="font-weight:400">/ AI</span></div><div class="status" id="status">● SYSTEM READY</div></header>
<main>
<section class="top">
<div class="panel corebox"><div class="core"><span>J.A.R.V.I.S</span></div></div>
<div class="panel">
<h1>GOOD EVENING.</h1><h2>PERSONAL AI ASSISTANT</h2>
<p class="muted">Your personal AI interface is online. Ask questions, work with code, or use voice input. AI services connect securely through the server.</p>
<div class="metrics"><div class="metric"><b id="clock">--:--</b><small>LOCAL TIME</small></div><div class="metric"><b id="date">---</b><small>DATE</small></div><div class="metric"><b id="connection">ONLINE</b><small>NETWORK</small></div></div>
<div class="tools">
<a href="https://www.youtube.com/" target="_blank" rel="noopener">YouTube</a>
<a href="https://github.com/" target="_blank" rel="noopener">GitHub</a>
<a href="https://www.google.com/" target="_blank" rel="noopener">Browser</a>
<button class="btn secondary" id="remind">Set reminder</button>
</div>
</div></section>
<section class="panel chat"><h2>NEURAL INTERFACE / CHAT</h2>
<div class="messages" id="messages"><div class="msg bot">Good evening. JARVIS systems are online. How may I assist you today?</div></div>
<div class="controls"><input class="field" id="prompt" placeholder="Type a message..." autocomplete="off"><button class="btn" id="send">SEND</button><button class="btn secondary" id="mic">MIC</button></div>
<p class="muted" style="font-size:12px;margin-bottom:0">Voice recognition depends on browser support and microphone permission.</p></section>
</main><footer>JARVIS AI • Secure server-side API integration</footer>
<script>
const $=id=>document.getElementById(id), messages=$('messages');
function tick(){const d=new Date();$('clock').textContent=d.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});$('date').textContent=d.toLocaleDateString();}tick();setInterval(tick,1000);
function add(text,who){const el=document.createElement('div');el.className='msg '+who;el.textContent=text;messages.appendChild(el);messages.scrollTop=messages.scrollHeight;return el}
async function send(){const text=$('prompt').value.trim();if(!text)return;$('prompt').value='';add(text,'user');$('send').disabled=true;$('status').textContent='● THINKING';
const pending=add('Processing your request...','bot');
try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});const data=await r.json();pending.textContent=data.reply||data.error||'No response received.';if(data.reply&&data.speech_endpoint){try{const sr=await fetch(data.speech_endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:data.reply})});if(sr.ok){const blob=await sr.blob();const audio=new Audio(URL.createObjectURL(blob));audio.play().catch(()=>{});}}catch(_){/* Text response remains available if speech fails. */}}}
catch(e){pending.textContent='Connection error. Check the server configuration and try again.';}
finally{$('send').disabled=false;$('status').textContent='● SYSTEM READY';}}
$('send').addEventListener('click',send);$('prompt').addEventListener('keydown',e=>{if(e.key==='Enter')send()});
$('mic').addEventListener('click',()=>{const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){add('Speech recognition is not supported in this browser.','bot');return;}const rec=new SR();rec.lang='en-US';rec.onresult=e=>{$('prompt').value=e.results[0][0].transcript;send()};rec.onerror=()=>add('Microphone recognition failed or permission was denied.','bot');rec.start();});
$('remind').addEventListener('click',()=>{const mins=prompt('Reminder in how many minutes?');if(mins===null)return;const n=Number(mins);if(!Number.isFinite(n)||n<1||n>1440){alert('Enter a number from 1 to 1440.');return;}if('Notification'in window&&Notification.permission==='default')Notification.requestPermission();setTimeout(()=>{if('Notification'in window&&Notification.permission==='granted')new Notification('JARVIS reminder');else alert('JARVIS reminder');},n*60000);alert('Reminder set for '+n+' minute(s). Keep this page open.');});
</script></body></html>"""

@app.get("/")
def home():
    return Response(PAGE, mimetype="text/html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "groq_configured": bool(GROQ_API_KEY),
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY),
        "voice_configured": bool(ELEVENLABS_VOICE_ID)
    })

@app.post("/api/chat")
def chat():
    if not GROQ_API_KEY:
        return jsonify(error="Groq is not configured. Add GROQ_API_KEY in your hosting environment variables."), 503
    body = request.get_json(silent=True) or {}
    message = str(body.get("message", "")).strip()
    if not message:
        return jsonify(error="Please enter a message."), 400
    if len(message) > 8000:
        return jsonify(error="Message is too long."), 413

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are JARVIS, a helpful, precise personal AI assistant. Reply in the language used by the user. Be honest about limitations. Never claim to control a device or account unless an authorized integration actually performed the action."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.6,
        "max_tokens": 1200
    }
    try:
        result = requests.post("https://api.groq.com/openai/v1/chat/completions",
                               headers=headers, json=payload, timeout=45)
        result.raise_for_status()
        reply = result.json()["choices"][0]["message"]["content"]
    except requests.RequestException:
        app.logger.exception("Groq request failed")
        return jsonify(error="The AI service is temporarily unavailable. Check the server logs."), 502
    except (KeyError, IndexError, ValueError):
        return jsonify(error="The AI service returned an unexpected response."), 502

    audio_url = None
    # Generate speech on demand in a separate endpoint; never expose the ElevenLabs key.
    return jsonify(reply=reply, audio_available=bool(ELEVENLABS_API_KEY),
                   speech_endpoint="/api/speech" if ELEVENLABS_API_KEY else None)

@app.post("/api/speech")
def speech():
    if not ELEVENLABS_API_KEY:
        return jsonify(error="ElevenLabs is not configured."), 503
    body = request.get_json(silent=True) or {}
    text = str(body.get("text", "")).strip()
    if not text or len(text) > 2500:
        return jsonify(error="Provide text between 1 and 2500 characters."), 400
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    try:
        result = requests.post(url,
            headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json",
                     "Accept": "audio/mpeg"},
            json={"text": text, "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
            timeout=60)
        result.raise_for_status()
        return Response(result.content, mimetype="audio/mpeg",
                        headers={"Cache-Control": "no-store"})
    except requests.RequestException:
        app.logger.exception("ElevenLabs request failed")
        return jsonify(error="Speech generation failed. Check ElevenLabs configuration."), 502

if __name__ == "__main__":
    # Use a production WSGI server in deployment; this is for local testing only.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
