'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User, ArrowLeft } from 'lucide-react';
import { addConversation } from '@/services/friendService';
import Cookies from 'js-cookie';

const AddConversationPage: React.FC = () => {
  const router = useRouter();
  const [context, setContext] = useState('');
  const [conversationDate, setConversationDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const token = Cookies.get('auth_token');
    if (!token) {
      router.push('/login');
      return;
    }

    const friendId = parseInt(window.location.pathname.split('/')[2], 10);
    if (isNaN(friendId)) {
      setError('Invalid friend ID');
      setLoading(false);
      return;
    }

    try {
      await addConversation(token, friendId, context, conversationDate);
      router.push(`/friend/${friendId}`);
    } catch (err) {
      setError('An error occurred while creating the conversation.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-16">
        <Link href={`/friend/${window.location.pathname.split('/')[2]}`} className="flex items-center text-blue-600 mb-4">
          <ArrowLeft size={20} className="mr-2" />
          Back to Friend Details
        </Link>
        <h1 className="text-2xl font-bold mb-4">Add New Conversation</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="context" className="block text-sm font-medium text-gray-700">Context</label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              rows={4}
              required
            />
          </div>
          <div>
            <label htmlFor="conversationDate" className="block text-sm font-medium text-gray-700">Conversation Date</label>
            <input
              type="datetime-local"
              id="conversationDate"
              value={conversationDate}
              onChange={(e) => setConversationDate(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
          </div>
          {error && <p className="text-red-500">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {loading ? 'Creating...' : 'Create Conversation'}
          </button>
        </form>
      </main>

      <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-lg">
        <div className="flex justify-around items-center h-16">
          <Link href="/home" className="flex flex-col items-center text-gray-600">
            <Home size={24} />
            <span className="text-xs">Home</span>
          </Link>
          <Link href="/chat" className="flex flex-col items-center text-gray-600">
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

export default AddConversationPage;
