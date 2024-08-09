'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User } from 'lucide-react';
import { ChatMessage, ChatResponse } from '@/interfaces/chat';
import { sendMessage } from '@/services/chatService';

const ChatPage: React.FC = () => {
  const router = useRouter();
  const [messages, setMessages] = useState<{ content: string; isSent: boolean }[]>([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const newMessage: ChatMessage = {
      user_id: 1, // 固定のユーザーID
      content: inputMessage,
    };

    setMessages([...messages, { content: inputMessage, isSent: true }]);
    setInputMessage('');

    try {
      const response = await sendMessage(newMessage);
      console.log(response); // レスポンスをコンソールに表示
      setMessages(prev => [...prev, { content: response.response.final_answer, isSent: false }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-16 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.isSent ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${message.isSent ? 'bg-blue-500 text-white' : 'bg-white'}`}>
                {message.content}
              </div>
            </div>
          ))}
        </div>
      </main>

      <div className="fixed bottom-16 left-0 right-0 bg-white p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="flex-grow px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            placeholder="Type a message..."
          />
          <button
            onClick={handleSendMessage}
            className="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Send
          </button>
        </div>
      </div>

      <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-lg">
        <div className="flex justify-around items-center h-16">
          <Link href="/home" className="flex flex-col items-center text-gray-600">
            <Home size={24} />
            <span className="text-xs">Home</span>
          </Link>
          <Link href="/chat" className="flex flex-col items-center text-indigo-600">
            <MessageCircle size={24} />
            <span className="text-xs">Chat</span>
          </Link>
          <Link href="/mypage" className="flex flex-col items-center text-gray-600">
            <User size={24} />
            <span className="text-xs">Mypage</span>
          </Link>
        </div>
      </nav>
    </div>
  );
};

export default ChatPage;
