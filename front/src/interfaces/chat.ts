// 送信用のメッセージ型
export interface ChatMessageSend {
  content: string;
}

// 受信用のメッセージ型（GET /chats のレスポンス）
export interface ChatMessageReceive {
  content: string;
  created_at: string;
  response: ChatResponse | null;
}

// チャットレスポンスの型
export interface ChatResponse {
  final_answer: string | null;
  created_at: string;
}

// チャットレスポンスの型
// export interface ChatResponse {
//   question_category: number;
//   response: {
//     who: string;
//     what: string;
//     related_subject: string | null;
//     status: string;
//     answer: string;
//     approximation: {
//       attribute: string;
//       value: string;
//     };
//     similarity_category: string;
//     final_answer: string;
//   };
// }
