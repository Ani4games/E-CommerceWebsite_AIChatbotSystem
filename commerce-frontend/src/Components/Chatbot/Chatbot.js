// Chatbot.js
import React, { useState } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I help you today?' }
  ]);

  const sendMessage = (text) => {
    setMessages([...messages, { sender: 'user', text }]);

    // Here you can call your backend/AI
    setTimeout(() => {
      setMessages((prev) => [...prev, { sender: 'bot', text: `You said: ${text}` }]);
    }, 500);
  };

  return (
    <div className="chatbot-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
      </div>
      <ChatInput sendMessage={sendMessage} />
    </div>
  );
};

export default Chatbot;
