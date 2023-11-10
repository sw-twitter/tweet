import React, { useEffect, useRef } from 'react';
import { Paper, List, ListItem, ListItemText, Typography, Divider } from '@mui/material';
import './ChatWindow.css';

const ChatWindow = ({ messages }) => {
    const endOfMessagesRef = useRef(null);


    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (

        <Paper className="chatWindow">
            <List>
                {messages.map((msg, index) => (
                    <React.Fragment key={index}>
                        <ListItem className={msg.author === 'user' ? "messageItemReverse" : "messageItem"} alignItems="flex-start">
                            <ListItemText
                                primary={
                                    <Typography
                                        className={`messageText ${msg.author === 'user' ? '' : 'botMessageText'}`}
                                    >
                                        {msg.text}
                                    </Typography>
                                }
                            />
                        </ListItem>
                        <Divider component="li" />
                    </React.Fragment>
                ))}
                <div ref={endOfMessagesRef} />
            </List>
        </Paper>

    );
};

export default ChatWindow;
