# GateFace 

<div>
  <p>GateFace is a <strong>Python-based project</strong> that uses <strong>Face ID recognition</strong> to open applications or URLs configured by the user. Think of it as a <em>face-unlock for your apps and tools</em> — once your face is recognized, GateFace automatically launches your chosen apps or websites.</p>
</div>

---

<div>
  <h2>✨ Features</h2>
  <ul>
    <li>Face ID authentication to trigger actions.</li>
    <li>Launches applications (e.g., Chrome, VS Code, Spotify).</li>
    <li>Opens URLs in your default browser.</li>
    <li>Fully customizable: choose which apps and URLs to launch.</li>
    <li>Supports launching <strong>multiple apps at once</strong>.</li>
  </ul>
</div>

---

<div>
  <h2>📦 Installation & Setup</h2>
  <ol>
    <li>
      <p>Clone the Repository:</p>
      <pre><code>git clone https://github.com/your-username/GateFace.git
cd GateFace</code></pre>
    </li>
    <li>
      <p>Install Dependencies (requires Python 3.8+):</p>
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
  </ol>
</div>

---

<div>
  <h2>⚙️ Configuration</h2>
  <p>You can configure which <strong>URLs</strong> and <strong>applications</strong> GateFace should open once your face is recognized.</p>

  <h3>1. Configure URLs (Line 10)</h3>
  <p>Edit the <code>URLS</code> array and add the URLs you want:</p>
  <pre><code>URLS = [
    "https://www.google.com",
    "https://music.youtube.com",
    "https://chat.openai.com"
]</code></pre>

  <h3>2. Configure Applications (Line 14)</h3>
  <p>Edit the <code>APPS</code> array and add the applications you want:</p>
  <pre><code>APPS = [
    "chrome": "Google Chrome",
    "code": "Visual Studio Code"
    "spotify": "Spotify"
]</code></pre>

  <h3>3. Configure App Launching (Line 63)</h3>
  <p>Modify the <code>subprocess.Popen</code> calls to launch the apps you configured:</p>
  <pre><code>subprocess.run(["open", "-a", APPLICATIONS["chrome"], *URLS])
subprocess.run(["open", "-a", APPLICATIONS["spotify"], *URLS])
subprocess.run(["open", "-a", APPLICATIONS["whatsapp"], *URLS])</code></pre>

  <p><strong>Tip:</strong> Make sure the names match your OS executable names.</p>

  <h3>4. URLs vs Applications</h3>
  <p>URLs will open in your default browser. If you don’t want this behavior, simply remove the <code>URLS</code> list.</p>

  <h3>5. Launch Multiple Applications</h3>
  <p>Duplicate <code>subprocess.Popen</code> calls for each additional app.</p>
</div>

---

<div>
  <h2>▶️ Running GateFace</h2>
  <p>After configuring, run the script:</p>
  <pre><code>python gateface.py</code></pre>
  <p>When your face is recognized, GateFace will open the configured URLs and launch the applications.</p>
</div>

---

<div>
  <h2>🖥️ Recommended Setup</h2>
  <ul>
    <li>Use <strong>Visual Studio Code</strong> with the Microsoft Python extension.</li>
    <li>Enable line numbers to quickly find Lines 10, 14, and 63.</li>
  </ul>
</div>

---

<div>
  <h2>🚀 Example Use Case</h2>
  <p>Face detected → Chrome opens with your daily tabs → VS Code launches → Spotify starts playing music.</p>
</div>
