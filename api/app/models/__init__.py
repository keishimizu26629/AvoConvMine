from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from .user import User
from .friend import Friend, Attribute, FriendAttribute
from .chat_history import ChatRequest, ChatResponse

# 共通のMetaDataオブジェクトを作成
metadata = MetaData()

# 新しいBaseModelを作成し、共通のmetadataを使用
BaseModel = declarative_base(metadata=metadata)

# 既存のモデルに新しいBaseModelを適用
User.__table__.metadata = metadata
Friend.__table__.metadata = metadata
Attribute.__table__.metadata = metadata
FriendAttribute.__table__.metadata = metadata
ChatRequest.__table__.metadata = metadata
ChatResponse.__table__.metadata = metadata

# 必要に応じて他のモデルも同様に処理
