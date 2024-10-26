import React, { useState, useEffect, useRef } from 'react'
import './styles/chatComponent.css'
import { FiRefreshCcw, FiSend, FiMic, FiTrash2, FiPaperclip, FiX } from 'react-icons/fi'

const ChatComponent = ({ messages, setMessages, sendMessage }) => {
  const [inputMessage, setInputMessage] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [attachedImages, setAttachedImages] = useState([])
  const [audioVisualization, setAudioVisualization] = useState([])
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const audioChunksRef = useRef([])
  const visualizationIntervalRef = useRef(null)


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = () => {
    if (isRecording) {
      stopRecording()
    } else if (inputMessage.trim() !== '' || attachedImages.length > 0) {
      const newMessage = {
        text: inputMessage.trim(),
        images: attachedImages,
        sender: 'user'
      }
      sendMessage(newMessage)
      setInputMessage('')
      setAttachedImages([])
    }
  }

  const handleReset = () => {
    setMessages([])
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const audioUrl = URL.createObjectURL(audioBlob)
        const newMessage = { audio: audioUrl, sender: 'user' }
        setMessages((prevMessages) => [...prevMessages, newMessage])
        if (socket) {
          socket.emit('audio_message', newMessage)
        }
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
      setAudioVisualization([])
      startVisualization()
    } catch (error) {
      console.error('Error accessing microphone:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      stopVisualization()
      if (audioContextRef.current) {
        audioContextRef.current.close()
      }
    }
  }

  const startVisualization = () => {
    if (!analyserRef.current) return
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
    
    visualizationIntervalRef.current = setInterval(() => {
      analyserRef.current.getByteFrequencyData(dataArray)
      const levels = Array.from(dataArray).slice(0, 10).map(value => value / 255)
      setAudioVisualization(prev => [...prev, ...levels].slice(-100))  // Keep last 100 values
    }, 100)
  }

  const stopVisualization = () => {
    if (visualizationIntervalRef.current) {
      clearInterval(visualizationIntervalRef.current)
    }
  }

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    const allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp']
    const validFiles = files.filter(file => allowedTypes.includes(file.type))

    if (validFiles.length !== files.length) {
      alert('Please upload only PNG, JPEG, GIF, or WebP images.')
    }

    Promise.all(validFiles.map(file => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = reject
        reader.readAsDataURL(file)
      })
    })).then(results => {
      setAttachedImages(prevImages => [...prevImages, ...results])
    })
  }

  const removeAttachedImage = (index) => {
    setAttachedImages(prevImages => prevImages.filter((_, i) => i !== index))
  }

  const AudioMessage = ({ audioUrl }) => {
    return (
      <div className="audio-message">
        <audio src={audioUrl} controls />
      </div>
    )
  }

  const ImageMessage = ({ images }) => {
    return (
      <div className="image-message">
        {images.map((imageUrl, index) => (
          <img key={index} src={imageUrl} alt={`User uploaded ${index + 1}`} />
        ))}
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
            <div className={`message ${message.sender}`}>
              {message.audio && <AudioMessage audioUrl={message.audio} />}
              {message.images && message.images.length > 0 && <ImageMessage images={message.images} />}
              {message.text && <div>{message.text}</div>}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat_input_container">
        {attachedImages.length > 0 && (
          <div className="attached-images-container">
            <div className="attached-images">
              {attachedImages.map((image, index) => (
                <div key={index} className="attached-image">
                  <img src={image} alt="Attached" />
                  <FiX onClick={() => removeAttachedImage(index)} className="remove-image" />
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="chat_input">
          {isRecording ? (
            <FiTrash2 onClick={stopRecording} className="icon" style={{marginRight: "0.5rem"}} />
          ) : (
            <FiPaperclip onClick={() => fileInputRef.current.click()} className="icon" style={{marginRight: "1rem"}} />
          )}
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileUpload}
            accept=".png,.jpg,.jpeg,.gif,.webp"
            multiple
          />
          {isRecording ? (
            <div className="audio-visualization">
              {audioVisualization.map((level, index) => (
                <div key={index} className="audio-bar" style={{ height: `${level * 100}%` }}></div>
              ))}
            </div>
          ) : (
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
            />
          )}
          <FiSend onClick={handleSendMessage} className="icon" />
        </div>
      </div>
    </div>
  )
}

export default ChatComponent
