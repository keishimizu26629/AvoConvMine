①Is Jon an engineer?
②What is Jon's occupation?
③Who is the engineer from Osaka?
④Can you tell me about Jon?

①リクエストしたUseridに該当するFriendAttribute.useridのデータかつ
②"who"の値をFriend.nameで調べて該当すればそのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
③"who"の値をFriend.nameで調べて該当しなければAttribute_idの29が”Name"だからそれに該当するFriendAttibute.friend_idを見つけて、そのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
④該当するFriendAttibute.valueをEmbeddingした配列を取得する。"what"をEmbeddingした値でコサイン類似度を求めて該当するものがあるか調べる。
⑤0.8以上であれば{"answer": "Yes", "approximation": null}で返し、0.5以上であれば{"answer": "No", "approximation": {attribute: , value: }},それ以外であれば0.5以上であれば{"answer": "No", "approximation": "No"}で返すようにして。

①Attribute.nameをEmbeddingした配列を取得する。"what"をEmbeddingした値でコサイン類似度を求めて該当するものがあるか調べる。
②"who"の値をFriend.nameで調べて該当すればそのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
③"who"の値をFriend.nameで調べて該当しなければAttribute_idの29が”Name"だからそれに該当するFriendAttibute.friend_idを見つけて、そのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
④①はコサイン類似度の値を0.8以上or0.5以上orその他で分類した判定値を返して。


①Attribute.nameをEmbeddingした配列を取得する。"what"をEmbeddingした値でコサイン類似度を求めて該当するものがあるか調べる。
②"who"の値をFriend.nameで調べて該当すればそのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
③"who"の値をFriend.nameで調べて該当しなければAttribute_idの29が”Name"だからそれに該当するFriendAttibute.friend_idを見つけて、そのFriend.idのFriendAttribute.{①のAttribute_id}で該当するものを返す。
④①はコサイン類似度の値を0.8以上or0.5以上orその他で分類した判定値を返して。



リクエストが{     "user_id": 1,     "content": "Is Kenji an engineer" } でそのレスポンinitial_responseが{     "who": "Kenji",     "what": "engineer",     "question_category": 2 }

の場合、

Answer: Yes or noを返さないといけない。

