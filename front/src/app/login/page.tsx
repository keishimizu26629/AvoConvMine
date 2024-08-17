'use client';

import React from 'react';
import Link from 'next/link';
import AuthForm from '@/components/AuthForm';
import { LogIn, UserPlus } from 'lucide-react';
let winston;
if (typeof window === 'undefined') {
  winston = require('winston');
}

const logger = winston ? winston.createLogger(/* your configuration */) : console;


logger.info('test1');

const LoginPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <main className="flex-grow flex flex-col justify-center p-4">
        <div className="max-w-md w-full mx-auto">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 mb-8">
            Sign in to your account
          </h2>
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <AuthForm isLogin={true} />
          </div>
        </div>
      </main>

      <nav className="bg-white shadow-lg">
        <div className="max-w-screen-xl mx-auto px-4">
          <div className="flex justify-between">
            <Link href="/login" className="flex items-center py-4 px-2">
              <LogIn className="h-6 w-6 text-indigo-600 mr-2" />
              <span className="font-semibold text-gray-500 text-lg">Login</span>
            </Link>
            <Link href="/register" className="flex items-center py-4 px-2">
              <UserPlus className="h-6 w-6 text-gray-500 mr-2" />
              <span className="font-semibold text-gray-500 text-lg">Register</span>
            </Link>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default LoginPage;
