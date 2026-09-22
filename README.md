# Foodie Friend - AI Restaurant Chatbot

**Foodie Friend** is a production-style AI conversational agent built for **Crave Lounge**, a restaurant based in Gujranwala, Pakistan. It lets customers browse the menu, ask questions, and place a complete food order — from item selection to a confirmed receipt — entirely through natural conversation with the Google Gemini API.

This project was built end-to-end as a personal/portfolio project to demonstrate practical Python backend development: API integration, session-based state management, input validation, and secure deployment — not just a wrapper around a chat API.

##  Live Demo

Try it here: **[https://foodie-chatbot-ir0y.onrender.com](https://foodie-chatbot-ir0y.onrender.com)**

*(Hosted on Render)*



##  Features

- **AI-Powered Conversations:** Uses the Google Gemini AI model to provide natural, human-like responses to customer queries.  
- **Menu Exploration:** Customers can browse specific categories (Fast Food, Chinese, Desi, etc.) or view the full menu.  
- **Automated Ordering System:** Collects user details (Name, Phone, and Address) and calculates the total bill including a flat delivery fee (Rs. 200).  
- **Receipt Generation:** Provides a detailed order summary and estimated delivery time (40-50 minutes) upon confirmation.  
- **Order Locking:** Once an order is confirmed, the system prevents adding new items to maintain order integrity.  
- **Multilingual Support:** Capable of interacting in multiple languages for a localized experience.  
- **Smart Fallbacks:** Politely handles unrelated queries and guides users back to the restaurant menu.  



##  What This Project Demonstrates

- **AI tool/function calling:** The Gemini model doesn't just chat — it calls real Python functions (`add_to_cart`, `remove_from_cart`, `prepare_order`, `confirm_order`, etc.) that run actual business logic. The AI proposes actions; this code validates and executes them.
- **Business logic kept out of the AI's hands:** Pricing, stock/quantity limits, phone number validation, and address checks all run in plain, testable Python (`bot/orders.py`) — the AI cannot invent a price or bypass a rule, it can only call functions that enforce them.
- **Session-based state management:** Each customer's cart and conversation history are stored server-side per session (`bot/orders.py`, `new_order_state`), with history trimmed to fit browser cookie limits without losing conversational context.
- **Input validation & defensive coding:** Phone numbers are validated against Pakistani mobile number formats with regex, addresses are length-checked, item quantities are bounds-checked, and message length is capped before it ever reaches the API.
- **Secure by design, not by accident:** Chat messages are rendered client-side using `textContent`/`createTextNode` only (never `innerHTML`), so the app is safe against XSS even if the AI response contains unexpected characters or HTML-like text.
- **Config-driven, environment-aware setup:** Settings (model name, delivery fee, history limits) live in `config.py`; secrets (`GOOGLE_API_KEY`, `SECRET_KEY`) are read from environment variables, never hardcoded, and `.env` is git-ignored.
- **Production deployment:** Configured with Gunicorn and a `Procfile` bound to a dynamic `$PORT`, deployed live on Render — not just tested locally.
- **Clean, modular structure:** Routes, order logic, menu data, and prompt engineering are separated into their own modules instead of one large script.

##  Tech Stack

- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript (vanilla, no framework)  
- **AI Model:** Google Gemini API, with function/tool calling  
- **Server:** Gunicorn  
- **Deployment:** Render  



## 📂 Project Structure

```text
Foodie-Friend-Bot/
├── app.py                 # Flask routes and Gemini integration
├── config.py               # Environment-driven settings
├── requirements.txt        # Dependencies
├── Procfile                 # Deployment command for Render
├── bot/
│   ├── orders.py            # Cart, validation, and order state logic (the AI's "tools")
│   ├── menu.py               # Menu data lookup helpers
│   └── prompt.py             # System prompt / AI instructions
├── data/
│   └── menu.json              # Menu items and prices
├── static/
│   ├── css/style.css           # UI styling
│   └── js/chat.js               # Chat rendering (XSS-safe: textContent only)
└── templates/
    └── index.html                # Frontend UI