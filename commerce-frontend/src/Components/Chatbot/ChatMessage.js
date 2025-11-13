const ChatMessage = ({ message }) => {
  return (
    <div className={message.sender === 'bot' ? 'bot-message' : 'user-message'}>
      {message.text}
    </div>
  );
};

export default ChatMessage;
// ChatMessage.js