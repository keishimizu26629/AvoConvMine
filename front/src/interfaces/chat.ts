export interface ChatMessage {
  user_id: number;
  content: string;
}

export interface ChatResponse {
  question_category: number;
  response: {
    who: string;
    what: string;
    related_subject: string | null;
    status: string;
    answer: string;
    approximation: {
      attribute: string;
      value: string;
    };
    similarity_category: string;
    final_answer: string;
  };
}
