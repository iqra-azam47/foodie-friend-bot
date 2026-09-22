# 🍔 Foodie Friend — Autonomous AI Restaurant Ordering Agent

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://foodie-friend-bot.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gemini API](https://img.shields.io/badge/Google_Gemini-Function_Calling-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

An end-to-end, production-oriented conversational commerce agent engineered for **Fire Flame** restaurant (Gujranwala, Pakistan). 

Unlike simple prompt-wrapper chatbots, **Foodie Friend** operates as an autonomous agent using **Gemini Tool/Function Calling** paired with a deterministic backend state engine. The LLM handles natural language interpretation while Python strictly controls business logic, order immutability, inventory limits, and transaction flows.

---

## 🌐 Live Application

* **Production Deployment:** [https://foodie-friend-bot.onrender.com/](https://foodie-friend-bot.onrender.com/)
* **Hosting Infrastructure:** Render (Gunicorn WSGI container)

---

## ⚡ System Architecture & Highlights

```text
[ User UI ] ──(JSON / Async Fetch)──► [ Flask Controller (app.py) ]
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
     [ Gemini LLM Agent ]                                         [ Order State Engine ]
  (Intent Parsing & Tool Call)                                  (tools.py / Local Session)
                 │                                                             │
                 └──────── Execute Python Tool Functions ─────────────────────►│
                               (add_to_cart, validate, lock)                   ▼
                                                                     [ Deterministic Bill ]
```

```markdown
### 1. Deterministic Business Logic vs. LLM Freedom

* **No Price Hallucination:** The LLM is strictly prohibited from computing mathematical sums or inventing menu items. All computations run inside deterministic Python routines (`bot/orders.py`).
* **Tool Invocation:** The model proposes actions via Gemini Function Calling (`add_to_cart`, `remove_from_cart`, `prepare_order`, `confirm_order`), which validate payload schemas against real data (`data/menu.json`).

### 2. State & Session Integrity

* **Cart State Isolation:** Orders are tracked in server-side session dictionaries rather than LLM conversational memory, preventing token degradation and context loss.
* **Order Freezing:** Once confirmed, state transitions to an immutable status to prevent post-order modifications.
* **Session Trimming:** Conversational buffers are systematically pruned to adhere to cookie byte bounds while maintaining immediate dialog context.

### 3. Defensive Engineering & Security

* **Regex Number Verification:** Mobile validation enforces Pakistani operator formats (`03xx-xxxxxxx` / `+92`).
* **XSS Neutralization:** Client-side message rendering avoids `innerHTML`, enforcing programmatic DOM generation (`document.createElement`, `textContent`) to neutralize malicious payloads.
* **Environment Isolation:** Zero credentials in version control; secrets load dynamically via environment injections.

---

## 🛠️ Tech Stack

| Domain | Technology |
| :--- | :--- |
| **Backend Framework** | Python / Flask |
| **LLM & Tool Calling** | Google GenAI SDK (`gemini-3.1-flash-lite`) |
| **State Management** | Flask Session Engine / JSON Datastore |
| **Web Server** | Gunicorn (Green Unicorn WSGI) |
| **Frontend UI** | Semantic HTML5, CSS3 Variables, Asynchronous Vanilla JS |
| **Deployment** | Render Cloud Platform |

---

## 📂 Codebase Layout

```text
Foodie-Friend-Bot/
├── bot/
│   ├── menu.py          # Structured menu query utilities
│   ├── orders.py        # Core transaction logic & agent tools
│   └── prompt.py        # System behavior & operational boundary prompts
├── data/
│   └── menu.json        # Single source of truth for items and pricing
├── static/
│   ├── css/style.css    # Clean interface styling
│   └── js/chat.js       # Resilient UI communication & DOM renderer
├── templates/
│   └── index.html       # Web client entrypoint
├── app.py               # WSGI routing, Gemini orchestrator, error fallbacks
├── config.py            # Centralized environment & app settings
├── Procfile             # Cloud process definition (Gunicorn)
└── requirements.txt     # Locked production dependencies
```

🚀 Local Development Setup
1. Clone Repository
Bash
git clone [https://github.com/iqra-azam47/foodie-friend-bot.git](https://github.com/iqra-azam47/foodie-friend-bot.git)
cd foodie-friend-bot
2. Configure Virtual Environment
Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Set Environment Variables
Create a .env file in the project root:

Code snippet
GOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secure_random_flask_secret
GEMINI_MODEL=gemini-3.1-flash-lite
5. Launch Development Server
Bash
python app.py
Access the client locally at http://127.0.0.1:5000.

👤 Author
Developer: Iqra Azam

GitHub: @iqra-azam47



