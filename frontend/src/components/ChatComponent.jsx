import React, { useState, useEffect, useRef } from 'react'
import './styles/chatComponent.css'
import { FiRefreshCcw, FiSend, FiMic, FiTrash2 } from 'react-icons/fi'
import { ReactMic } from 'react-mic'

const ChatComponent = ({ socket }) => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (socket) {
      socket.on('agent_response', (data) => {
        setMessages((prevMessages) => [...prevMessages, { text: data.message, sender: 'agent' }])
      })

      socket.on('message', (data) => {
        setMessages((prevMessages) => [...prevMessages, { text: data.message, sender: 'agent' }])
      })

      socket.on('error', (data) => {
        console.error('Socket error:', data.message)
      })
    }
  }, [socket])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = () => {
    if (inputMessage.trim() !== '' && socket) {
      setMessages((prevMessages) => [...prevMessages, { text: inputMessage, sender: 'user' }])
      socket.emit('user_message', { message: inputMessage })
      setInputMessage('')
    }
  }

  const handleReset = () => {
    if (socket) {
      socket.emit('reset')
      setMessages([])
    }
  }

  const startRecording = () => {
    setIsRecording(true)
  }

  const stopRecording = () => {
    setIsRecording(false)
  }

  const onData = (recordedBlob) => {
    console.log('chunk of real-time data is: ', recordedBlob)
  }

  const onStop = (recordedBlob) => {
    console.log('recordedBlob is: ', recordedBlob)
    const url = URL.createObjectURL(recordedBlob.blob)
    setMessages((prevMessages) => [...prevMessages, { audio: url, sender: 'user' }])
    // You can also send this blob to your server if needed
    // socket.emit('audio_message', { audio: recordedBlob.blob })
  }

  const AudioMessage = ({ audioUrl }) => {
    return (
      <div className="audio-message">
        <audio src={audioUrl} controls />
      </div>
    )
  }

  return (
    <div className="chat">
      <div className='chat_header'>
        <h2 style={{margin: 0}}>Talk to Styler</h2>
        <FiRefreshCcw onClick={handleReset} style={{ cursor: 'pointer' }} />
      </div>
      <div className="chat_messages">
        {messages.map((message, index) => (
          <div key={index} className={`message_container ${message.sender}`}>
            {message.audio ? (
              <AudioMessage audioUrl={message.audio} />
            ) : (
              <div className={`message ${message.sender}`}>
                {message.text}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        {isRecording ? (
          <>
            <ReactMic
              record={isRecording}
              className="sound-wave"
              onStop={onStop}
              onData={onData}
              strokeColor="#000000"
              backgroundColor="#FF4081"
            />
            <FiTrash2 onClick={stopRecording} className="icon" />
          </>
        ) : (
          <>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
            />
            <FiMic onClick={startRecording} className="icon" />
          </>
        )}
        <FiSend onClick={isRecording ? stopRecording : handleSendMessage} className="icon" />
      </div>
    </div>
  )
}

export default ChatComponent
