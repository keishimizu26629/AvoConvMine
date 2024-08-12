'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User, Plus } from 'lucide-react';
import { FriendDetails } from '@/interfaces/friend';
import { getFriendDetails } from '@/services/friendService';
import Cookies from 'js-cookie';

const FriendDetailsPage: React.FC = () => {
  const router = useRouter();
  const [friendDetails, setFriendDetails] = useState<FriendDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { friendId } = useParams();

  useEffect(() => {
    const fetchFriendDetails = async () => {
      const token = Cookies.get('auth_token');
      if (!token) {
        router.push('/login');
        return;
      }

      const friendId = parseInt(window.location.pathname.split('/').pop() || '', 10);
      if (isNaN(friendId)) {
        setError('Invalid friend ID');
        setLoading(false);
        return;
      }

      try {
        const details = await getFriendDetails(token, friendId);
        setFriendDetails(details);
      } catch (err) {
        setError('Failed to fetch friend details');
      } finally {
        setLoading(false);
      }
    };

    fetchFriendDetails();
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
        <h1 className="text-2xl font-bold mb-4">{friendDetails?.friend_name}</h1>
        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Friend Details</h3>
          </div>
          <div className="border-t border-gray-200">
            <dl>
              {friendDetails?.attributes.map((attr, index) => (
                <div key={index} className={`${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'} px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6`}>
                  <dt className="text-sm font-medium text-gray-500">{attr.attribute_name}</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{attr.value}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>

        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-4">
          <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Conversations</h3>
            <Link href={`/friend/${window.location.pathname.split('/').pop()}/add-conversation`} className="bg-blue-500 text-white rounded-full p-2">
              <Plus size={20} />
            </Link>
          </div>
          <div className="border-t border-gray-200">
            <ul className="divide-y divide-gray-200">
              {friendDetails?.conversations.map((conversation, index) => (
                <li key={index} className="px-4 py-4">
                  <Link href={`/friend/${window.location.pathname.split('/').pop()}/conversation/${index}`} className="text-blue-600 hover:underline">
                    {new Date(conversation.conversation_date).toLocaleString()}
                  </Link>
                </li>
              ))}
            </ul>
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

export default FriendDetailsPage;
