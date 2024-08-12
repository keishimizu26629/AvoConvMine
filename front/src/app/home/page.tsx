'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User, Plus } from 'lucide-react';
import { Friend } from '@/interfaces/friend';
import { getFriends } from '@/services/friendService';
import Cookies from 'js-cookie';

const HomePage: React.FC = () => {
  const router = useRouter();
  const [friends, setFriends] = useState<Friend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFriends = async () => {
      const token = Cookies.get('auth_token');
      if (!token) {
        router.push('/login');
        return;
      }

      try {
        const data = await getFriends(token);
        setFriends(data);
      } catch (err) {
        if (err instanceof Error && err.message === 'Invalid credentials') {
          Cookies.remove('auth_token');
          router.push('/login');
        } else {
          setError('An error occurred while fetching friends.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchFriends();
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
        <h1 className="text-2xl font-bold mb-4">Friend List</h1>
        <ul className="space-y-2">
          {friends.map((friend) => (
            <li key={friend.id} className="bg-white p-4 rounded shadow">
              <Link href={`/friend/${friend.id}`} className="text-blue-500 hover:underline">
                {friend.name}
              </Link>
            </li>
          ))}
        </ul>
      </main>

      <Link href="/create-friend" className="fixed bottom-20 right-4 bg-blue-500 text-white rounded-full p-4 shadow-lg">
        <Plus size={24} />
      </Link>

      <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-lg">
        <div className="flex justify-around items-center h-16">
          <Link href="/home" className="flex flex-col items-center text-indigo-600">
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

export default HomePage;
