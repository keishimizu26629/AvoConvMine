/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  publicRuntimeConfig: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL,
  },
  // SASSを使用している場合のみ、以下のオプションを保持してください
  // sassOptions: {
  //   includePaths: [path.join(process.cwd(), 'src/styles')],
  // },
};

export default nextConfig;
