import React, { useState } from 'react';
import { TextareaAutosize, Button } from '@mui/material';
import './ChatInput.css';

const ChatInput = ({ onSendMessage }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSendMessage(message);
        setMessage('');
    };

    return (
        <form onSubmit={handleSubmit} className="chatInputForm">
            <TextareaAutosize
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                className="chatInputField"
                minRows={1}
                maxRows={4}
                style={{ width: '100%' }}
            />
            <Button variant="contained" color="primary" type="submit">
                Send
            </Button>
        </form>
    );
};

export default ChatInput;



