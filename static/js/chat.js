// Chat page logic: sends messages to /chat and shows the replies safely.

const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

function fillBotBubble(bubble, text) {
    const safeText = (text === undefined || text === null) ? "No response received" : String(text);
    const cleaned = safeText.replace(/^[ \t]*[*-] /gm, '\u2022 ');
    const parts = cleaned.split(/\*\*(.+?)\*\*/g);
    parts.forEach(function(part, i) {
        if (i % 2 === 1) {
            const bold = document.createElement('strong');
            bold.textContent = part;
            bubble.appendChild(bold);
        } else {
            bubble.appendChild(document.createTextNode(part));
        }
    });
}

function addMessage(sender, text, isError) {
    const box = document.createElement('div');
    box.className = 'message-box';

    const bubble = document.createElement('div');
    if (sender === 'user') {
        bubble.className = 'user-message';
        bubble.textContent = text;
    } else {
        bubble.className = 'bot-message';
        fillBotBubble(bubble, text);
    }
    if (isError) {
        bubble.style.color = 'red';
    }

    box.appendChild(bubble);
    chatHistory.appendChild(box);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return box;
}

function setBusy(busy) {
    userInput.disabled = busy;
    sendBtn.disabled = busy;
    if (!busy) {
        userInput.focus();
    }
}

async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage === '' || sendBtn.disabled) return;

    addMessage('user', userMessage);
    userInput.value = '';
    setBusy(true);

    const typingIndicator = addMessage('bot', '...');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        });

        let data = {};
        try {
            data = await response.json();
        } catch (parseError) {
            console.error("JSON parse error:", parseError);
        }

        typingIndicator.remove();

        const botReply = data.response || data.reply || data.message || data.error;

        if (response.ok && botReply) {
            addMessage('bot', botReply);
        } else {
            addMessage('bot', botReply || 'Sorry, something went wrong. Please try again.', true);
        }
    } catch (error) {
        console.error('Network Error:', error);
        typingIndicator.remove();
        addMessage('bot', 'Cannot reach the server. Please check your connection and try again.', true);
    } finally {
        setBusy(false);
    }
}