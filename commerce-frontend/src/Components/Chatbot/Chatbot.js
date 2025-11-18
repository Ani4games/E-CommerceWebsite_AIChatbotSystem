import React, { useState } from "react";
import axios from "axios"; 
import "./ChatBot.css";

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello 👋! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");

  // 🔵 Send message to backend and get chatbot response
  const sendToBackend = async (userText) => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        user_id: "web_user",
        message: userText,
      });

      return res.data.response;
    } catch (error) {
      return "⚠️ Error contacting server.";
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    const userText = input;
    setInput("");

    // 🟡 Show temporary "typing..." indicator
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: "Typing..." },
    ]);

    // 🔵 Get response from backend
    const botReply = await sendToBackend(userText);

    // Replace "typing..." message with real reply
    setMessages((prev) => {
      const updated = [...prev];
      updated.pop(); // remove "typing..."
      return [...updated, { sender: "bot", text: botReply }];
    });
  };

  return (
    <div>
      {/* Chat toggle button */}
      <div className="chatbot-toggle" onClick={() => setIsOpen(!isOpen)}>
        💬
      </div>

      {/* Chat window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">ShopSmart Assistant 🤖</div>

          <div className="chatbot-body">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${
                  msg.sender === "user" ? "user" : "bot"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
