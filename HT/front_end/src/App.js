import React, { useState, useEffect } from 'react';
import ChatWindow from './UI/ChatWindow';
import ChatInput from './UI/ChatInput';
import { Container, Typography, CssBaseline } from '@mui/material';
const App = () => {


  const [messages, setMessages] = useState([]);
  useEffect(() => {
    console.log("Updated messages:", messages);
  }, [messages]);

  const handleSendMessage = async (newMessage) => {

    setMessages(prevMessages => [...prevMessages, { text: newMessage, author: 'user' }]);
    console.log("After adding user message:", messages);


    try {

      const response = await fetch('SERVER_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: newMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();


      setMessages(messages => [...messages, { text: data.response, author: 'bot' }]);
    } catch (error) {
      console.error("Failed to send message:", error);
    }


  };
  return (
    <Container component="main" maxWidth="sm">
      <CssBaseline />
      <Typography component="h1" variant="h4" align="center" style={{ margin: '20px 0' }}>
        Chatbot
      </Typography>
      <ChatWindow messages={messages} />
      <ChatInput onSendMessage={handleSendMessage} />
    </Container>
  );
};

export default App;
