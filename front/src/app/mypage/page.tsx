'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';
import Link from 'next/link';
import { Home, MessageCircle, User, LogOut } from 'lucide-react';

const MyPage: React.FC = () => {
  const router = useRouter();

  const handleLogout = () => {
    Cookies.remove('auth_token');
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-16">
        <h1 className="text-2xl font-bold mb-4">My Page</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Logout
        </button>
        {/* その他のユーザー情報や設定などをここに追加 */}
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
          <Link href="/mypage" className="flex flex-col items-center text-indigo-600">
            <User size={24} />
            <span className="text-xs">Mypage</span>
          </Link>
        </div>
      </nav>
    </div>
  );
};

export default MyPage;
