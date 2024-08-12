'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User } from 'lucide-react';
import { ChatMessageReceive, ChatMessageSend } from '@/interfaces/chat';
import { getChats, sendMessage } from '@/services/chatService';
import Cookies from 'js-cookie';

const ChatPage: React.FC = () => {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessageReceive[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    const fetchChats = async () => {
      const token = Cookies.get('auth_token');
      console.log(token)
      if (!token) {
        router.push('/login');
        return;
      }
      try {
        const response = await getChats(token);
        console.log('Received chat data:', JSON.stringify(response, null, 2));
        setMessages(response);
      } catch (error) {
        console.error('Failed to fetch chats:', error);
      } finally {
        setInitialLoading(false);
      }
    };

    fetchChats();
  }, [router]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const token = Cookies.get('auth_token');
    if (!token) {
      router.push('/login');
      return;
    }

    setLoading(true);
    try {
      const messageToSend: ChatMessageSend = { content: inputMessage };
      const newMessage = await sendMessage(messageToSend, token);
      setMessages(prev => [...prev, newMessage]);
      setInputMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-32 overflow-y-auto">
        <div className="space-y-4">
          {messages && messages.length > 0 ? (
            messages.map((message, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-end">
                  <div className="max-w-xs lg:max-w-md px-4 py-2 bg-blue-500 text-white rounded-lg">
                    {message.content}
                    <div className="text-xs text-gray-300 mt-1">{new Date(message.created_at).toLocaleString()}</div>
                  </div>
                </div>
                {message.response && message.response.final_answer && (
                  <div className="flex justify-start">
                    <div className="max-w-xs lg:max-w-md px-4 py-2 bg-white rounded-lg text-black">
                      {message.response.final_answer}
                      <div className="text-xs text-gray-500 mt-1">{new Date(message.response.created_at).toLocaleString()}</div>
                    </div>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="text-center text-gray-500">No messages yet.</div>
          )}
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
            disabled={loading}
            className="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Sending...' : 'Send'}
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
