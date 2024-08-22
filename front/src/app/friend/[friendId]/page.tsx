'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Home, MessageCircle, User, Plus, Pencil, Trash2 } from 'lucide-react';
import { FriendDetails, FriendAttribute } from '@/interfaces/friend';
import { getFriendDetails, updateFriendDetails } from '@/services/friendService';
import Cookies from 'js-cookie';

const FriendDetailsPage: React.FC = () => {
  const router = useRouter();
  const [friendDetails, setFriendDetails] = useState<FriendDetails | null>(null);
  const [editingAttributes, setEditingAttributes] = useState<FriendAttribute[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchFriendDetails();
  }, []);

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
      setEditingAttributes(details.attributes);
    } catch (err) {
      setError('Failed to fetch friend details');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditingAttributes(friendDetails?.attributes || []);
  };

  const handleSave = async () => {
    const token = Cookies.get('auth_token');
    const friendId = parseInt(window.location.pathname.split('/').pop() || '', 10);
    if (!token || isNaN(friendId)) return;

    try {
      await updateFriendDetails(token, friendId, editingAttributes);
      setFriendDetails(prev => prev ? {...prev, attributes: editingAttributes} : null);
      setIsEditing(false);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      setSaveError('Failed to update friend details');
      setTimeout(() => setSaveError(null), 3000);
    }
  };

  const handleAttributeChange = (index: number, field: 'attribute_name' | 'value', newValue: string) => {
    const newAttributes = [...editingAttributes];
    newAttributes[index][field] = newValue;
    setEditingAttributes(newAttributes);
  };

  const handleDeleteAttribute = (index: number) => {
    if (confirm('Are you sure you want to delete this attribute?')) {
      const newAttributes = editingAttributes.filter((_, i) => i !== index);
      setEditingAttributes(newAttributes);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow p-4 mb-16">
        <h1 className="text-2xl font-bold mb-4 text-indigo-400">{friendDetails?.friend_name}</h1>

        {saveSuccess && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">Friend details updated successfully.</span>
          </div>
        )}

        {saveError && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{saveError}</span>
          </div>
        )}

        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
          <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Friend Details</h3>
            {!isEditing && (
              <button onClick={handleEdit} className="text-blue-600">
                <Pencil size={20} />
              </button>
            )}
          </div>
          <div className="border-t border-gray-200">
            <dl>
              {editingAttributes.map((attr, index) => (
                <div key={index} className={`${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'} px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6`}>
                  {isEditing ? (
                    <>
                      <input
                        className="text-sm font-medium text-gray-500 border rounded px-2 py-1"
                        value={attr.attribute_name}
                        onChange={(e) => handleAttributeChange(index, 'attribute_name', e.target.value)}
                      />
                      <input
                        className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-1 border rounded px-2 py-1"
                        value={attr.value}
                        onChange={(e) => handleAttributeChange(index, 'value', e.target.value)}
                      />
                      <button onClick={() => handleDeleteAttribute(index)} className="text-red-500">
                        <Trash2 size={20} />
                      </button>
                    </>
                  ) : (
                    <>
                      <dt className="text-sm font-medium text-gray-500">{attr.attribute_name}</dt>
                      <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{attr.value}</dd>
                    </>
                  )}
                </div>
              ))}
            </dl>
          </div>
          {isEditing && (
            <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
              <button onClick={handleCancel} className="mr-2 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
                Cancel
              </button>
              <button onClick={handleSave} className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Save
              </button>
            </div>
          )}
        </div>

        {/* Conversations section */}
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

      {/* Navigation bar */}
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
