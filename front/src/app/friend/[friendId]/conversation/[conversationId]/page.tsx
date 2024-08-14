'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User, ArrowLeft } from 'lucide-react';
import { FriendDetails } from '@/interfaces/friend';
import { getFriendDetails } from '@/services/friendService';
import Cookies from 'js-cookie';

const ConversationDetailPage: React.FC = () => {
  const router = useRouter();
  const [conversation, setConversation] = useState<{ context: string; conversation_date: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConversationDetails = async () => {
      const token = Cookies.get('auth_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const pathParts = window.location.pathname.split('/');
      const friendName = pathParts[pathParts.length - 3];
      const conversationId = parseInt(pathParts[pathParts.length - 1], 10);

      if (isNaN(conversationId)) {
        setError('Invalid conversation ID');
        setLoading(false);
        return;
      }

      try {
        const details = await getFriendDetails(token, 0); // You might need to adjust this to get the correct friend ID
        if (details && details.conversations && details.conversations[conversationId]) {
          setConversation(details.conversations[conversationId]);
        } else {
          setError('Conversation not found');
        }
      } catch (err) {
        setError('Failed to fetch conversation details');
      } finally {
        setLoading(false);
      }
    };

    fetchConversationDetails();
  }, [router]);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-16">
        <Link href={`/friend/${window.location.pathname.split('/')[2]}`} className="flex items-center text-blue-600 mb-4">
          <ArrowLeft size={20} className="mr-2" />
          Back to Friend Details
        </Link>
        <h1 className="text-2xl font-bold mb-4">Conversation Detail</h1>
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {new Date(conversation?.conversation_date || '').toLocaleString()}
            </h3>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl className="sm:divide-y sm:divide-gray-200">
              <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt className="text-sm font-medium text-gray-500">Context</dt>
                <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{conversation?.context}</dd>
              </div>
            </dl>
          </div>
        </div>
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

export default ConversationDetailPage;
