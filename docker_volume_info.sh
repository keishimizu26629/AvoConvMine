#!/bin/bash

# echo "Volume Name | Size | Used By"
# echo "------------ | ---- | -------"

# docker volume ls -q | while read vol; do
#     # ボリュームのサイズを取得
#     size=$(docker run --rm -v $vol:/vol alpine du -sh /vol | cut -f1)

#     # ボリュームを使用しているコンテナを取得
#     used_by=$(docker ps -a --filter volume=$vol --format '{{.Names}} ({{.Image}})')

#     if [ -z "$used_by" ]; then
#         used_by="Not in use"
#     fi

#     echo "$vol | $size | $used_by"
# done

#!/bin/bash

echo "Image ID | Repository | Tag | Size | Created | Used By"
echo "--------- | ---------- | --- | ---- | ------- | -------"

docker images --format "{{.ID}}|{{.Repository}}|{{.Tag}}|{{.Size}}|{{.CreatedSince}}" | while IFS='|' read -r id repo tag size created; do
    # イメージを使用しているコンテナを取得
    used_by=$(docker ps -a --filter ancestor=$repo:$tag --format '{{.Names}}' | paste -sd "," -)

    if [ -z "$used_by" ]; then
        used_by="Not in use"
    fi

    echo "$id | $repo | $tag | $size | $created | $used_by"
done
