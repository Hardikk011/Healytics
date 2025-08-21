import React, { useState } from 'react';
import axios from 'axios';
import { MessageCircle } from "lucide-react"

const AIChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages([...messages, { sender: 'user', text: input }]);
    try {
      const res = await axios.post('/api/chat/', { message: input });
      setMessages(prev => [...prev, { sender: 'ai', text: res.data.reply }]);
    } catch (err) {
      let errorMsg = 'Sorry, something went wrong.';
      if (err.response && err.response.data && err.response.data.reply) {
        errorMsg = err.response.data.reply;
      } else if (err.response && err.response.data && err.response.data.error) {
        errorMsg = err.response.data.error;
      }
      setMessages(prev => [...prev, { sender: 'ai', text: errorMsg }]);
    }
    setInput('');
    setLoading(false);
  };

  return React.createElement(
    'div',
    { className: "max-w-xl mx-auto py-8 px-4" },
    React.createElement(
      'div',
      { className: "flex items-center space-x-3 mb-6" },
      React.createElement(MessageCircle, { className: "h-8 w-8 text-blue-600" }),
      React.createElement(
        'div',
        null,
        React.createElement('h1', { className: "text-2xl font-bold text-gray-900" }, "AI Career Assistant"),
        React.createElement('p', { className: "text-gray-600" }, "Get personalized career advice and guidance")
      )
    ),
    React.createElement(
      'div',
      { className: "border rounded-lg p-4 mb-4 bg-white min-h-[300px]" },
      messages.map((msg, idx) =>
        React.createElement(
          'div',
          {
            key: idx,
            className: `mb-2 text-${msg.sender === 'user' ? 'right' : 'left'}`
          },
          React.createElement(
            'span',
            {
              className: `inline-block px-3 py-2 rounded ${msg.sender === 'user' ? 'bg-primary-100 text-primary-800' : 'bg-gray-100 text-gray-800'}`
            },
            msg.text
          )
        )
      ),
      loading && React.createElement('div', { className: "text-gray-500" }, "AI is typing...")
    ),
    React.createElement(
      'div',
      { className: "flex gap-2" },
      React.createElement('input', {
        type: "text",
        className: "flex-1 border rounded px-3 py-2",
        value: input,
        onChange: e => setInput(e.target.value),
        onKeyDown: e => e.key === 'Enter' ? sendMessage() : null,
        placeholder: "Type your message...",
        disabled: loading
      }),
      React.createElement(
        'button',
        {
          className: "bg-primary-500 text-white px-4 py-2 rounded",
          onClick: sendMessage,
          disabled: loading
        },
        "Send"
      )
    )
  );
}

export default AIChatbot
