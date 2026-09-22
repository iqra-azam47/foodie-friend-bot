🍔 Foodie Friend — Autonomous AI Restaurant Ordering AgentAn end-to-end, production-oriented conversational commerce agent engineered for Fire Flame restaurant (Gujranwala, Pakistan).Unlike simple prompt-wrapper chatbots, Foodie Friend operates as an autonomous agent using Gemini Tool/Function Calling paired with a deterministic backend state engine. The LLM handles natural language interpretation while Python strictly controls business logic, order immutability, inventory limits, and transaction flows.🌐 Live ApplicationProduction Deployment: https://foodie-friend-bot.onrender.com/Hosting Infrastructure: Render (Gunicorn WSGI container)⚡ System Architecture & HighlightsPlaintext[ User UI ] ──(JSON / Async Fetch)──► [ Flask Controller (app.py) ]
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
     [ Gemini LLM Agent ]                                         [ Order State Engine ]
  (Intent Parsing & Tool Call)                                  (tools.py / Local Session)
                 │                                                             │
                 └──────── Execute Python Tool Functions ─────────────────────►│
                               (add_to_cart, validate, lock)                   ▼
                                                                     [ Deterministic Bill ]
1. Deterministic Business Logic vs. LLM FreedomNo Price Hallucination: The LLM is strictly prohibited from computing mathematical sums or inventing menu items. All computations run inside deterministic Python routines (bot/orders.py).Tool Invocation: The model proposes actions via Gemini Function Calling (add_to_cart, remove_from_cart, prepare_order, confirm_order), which validate payload schemas against real data (data/menu.json).2. State & Session IntegrityCart State Isolation: Orders are tracked in server-side session dictionaries rather than LLM conversational memory, preventing token degradation and context loss.Order Freezing: Once confirmed, state transitions to an immutable status to prevent post-order modifications.Session Trimming: Conversational buffers are systematically pruned to adhere to cookie byte bounds while maintaining immediate dialog context.3. Defensive Engineering & SecurityRegex Number Verification: Mobile validation enforces Pakistani operator formats (03xx-xxxxxxx / +92).XSS Neutralization: Client-side message rendering avoids innerHTML, enforcing programmatic DOM generation (document.createElement, textContent) to neutralize malicious payloads.Environment Isolation: Zero credentials in version control; secrets load dynamically via environment injections.🛠️ Tech StackDomainTechnologyBackend FrameworkPython / FlaskLLM & Tool CallingGoogle GenAI SDK (gemini-3.1-flash-lite)State ManagementFlask Session Engine / JSON DatastoreWeb ServerGunicorn (Green Unicorn WSGI)Frontend UISemantic HTML5, CSS3 Variables, Asynchronous Vanilla JSDeploymentRender Cloud Platform📂 Codebase LayoutPlaintextFoodie-Friend-Bot/
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
🚀 Local Development Setup1. Clone RepositoryBashgit clone https://github.com/iqra-azam47/foodie-friend-bot.git
cd foodie-friend-bot
2. Configure Virtual EnvironmentBashpython -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
3. Install DependenciesBashpip install -r requirements.txt
4. Set Environment VariablesCreate a .env file in the project root:Code snippetGOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secure_random_flask_secret
GEMINI_MODEL=gemini-3.1-flash-lite
5. Launch Development ServerBashpython app.py
Access the client locally at [http://127.0.0.1:5000](http://127.0.0.1:5000).👤 AuthorDeveloper: Iqra AzamGitHub: @iqra-azam47
