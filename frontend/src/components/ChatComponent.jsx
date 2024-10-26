import React, { useState, useEffect, useRef } from 'react'
import './styles/chatComponent.css'
import { FiRefreshCcw, FiSend, FiMic, FiStopCircle, FiPaperclip, FiX } from 'react-icons/fi'

const ChatComponent = ({ socket }) => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [attachedImage, setAttachedImage] = useState(null)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])

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
    if ((inputMessage.trim() !== '' || attachedImage) && socket) {
      const newMessage = {
        text: inputMessage,
        image: attachedImage,
        sender: 'user'
      }
      setMessages((prevMessages) => [...prevMessages, newMessage])
      socket.emit('user_message', newMessage)
      setInputMessage('')
      setAttachedImage(null)
    }
  }

  const handleReset = () => {
    if (socket) {
      socket.emit('reset')
      setMessages([])
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const audioUrl = URL.createObjectURL(audioBlob)
        setMessages((prevMessages) => [...prevMessages, { audio: audioUrl, sender: 'user' }])
        // You can also send this blob to your server if needed
        // socket.emit('audio_message', { audio: audioBlob })
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error accessing microphone:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      const allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp']
      if (allowedTypes.includes(file.type)) {
        const reader = new FileReader()
        reader.onload = (e) => {
          setAttachedImage(e.target.result)
        }
        reader.readAsDataURL(file)
      } else {
        alert('Please upload only PNG, JPEG, GIF, or WebP images.')
      }
    }
  }

  const removeAttachedImage = () => {
    setAttachedImage(null)
  }

  const AudioMessage = ({ audioUrl }) => {
    return (
      <div className="audio-message">
        <audio src={audioUrl} controls />
      </div>
    )
  }

  const ImageMessage = ({ imageUrl }) => {
    return (
      <div className="image-message">
        <img src={imageUrl} alt="User uploaded" style={{ maxWidth: '100%', maxHeight: '200px' }} />
      </div>
    )
  }

  return (
    <div className="chat">
      <div className='chat_header'>
        <h4 style={{margin: 0, fontSize: '1.2rem'}}>Chat</h4>
        <FiRefreshCcw onClick={handleReset} style={{ cursor: 'pointer' }} />
      </div>
      <div className="chat_messages">
        {messages.map((message, index) => (
          <div key={index} className={`message_container ${message.sender}`}>
            {message.audio ? (
              <AudioMessage audioUrl={message.audio} />
            ) : (
              <div className={`message ${message.sender}`}>
                {message.image && <ImageMessage imageUrl={message.image} />}
                {message.text && <div>{message.text}</div>}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat_input_container">
        {attachedImage && (
          <div className="attached-image">
            <img src={attachedImage} alt="Attached" style={{ maxWidth: '100px', maxHeight: '100px' }} />
            <FiX onClick={removeAttachedImage} className="remove-image" />
          </div>
        )}
        <div className="chat_input">
          <FiPaperclip onClick={() => fileInputRef.current.click()} className="icon" />
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileUpload}
            accept=".png,.jpg,.jpeg,.gif,.webp"
          />
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
          />
          {isRecording ? (
            <FiStopCircle onClick={stopRecording} className="icon recording" />
          ) : (
            <FiMic onClick={startRecording} className="icon" />
          )}
          <FiSend onClick={handleSendMessage} className="icon" />
        </div>
      </div>
    </div>
  )
}

export default ChatComponent
