export interface Friend {
  name: string;
  user_id: number;
  id: number;
}

export interface FriendAttribute {
  attribute_name: string;
  value: string;
}

export interface Conversation {
  context: string;
  conversation_date: string;
}

export interface FriendDetails {
  friend_name: string;
  attributes: FriendAttribute[];
  conversations: Conversation[];
}
