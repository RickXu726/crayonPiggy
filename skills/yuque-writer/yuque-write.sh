#!/bin/bash
# 语雀写入脚本

set -e

# 配置
YUQUE_TOKEN="${YUQUE_TOKEN:-}"
YUQUE_API="https://www.yuque.com/api/v2"

# 解析参数
TITLE=""
CONTENT=""
REPO_ID=""
SLUG=""
PUBLIC=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        --repo-id)
            REPO_ID="$2"
            shift 2
            ;;
        --slug)
            SLUG="$2"
            shift 2
            ;;
        --public)
            PUBLIC=1
            shift
            ;;
        *)
            echo "未知参数：$1"
            exit 1
            ;;
    esac
done

# 验证必填参数
if [[ -z "$YUQUE_TOKEN" ]]; then
    echo "错误：未设置 YUQUE_TOKEN，请在 TOOLS.md 中配置语雀 API Token"
    exit 1
fi

if [[ -z "$TITLE" ]]; then
    echo "错误：--title 是必填参数"
    exit 1
fi

if [[ -z "$CONTENT" ]]; then
    echo "错误：--content 是必填参数"
    exit 1
fi

if [[ -z "$REPO_ID" ]]; then
    echo "错误：--repo-id 是必填参数（或在 TOOLS.md 中配置默认知识库 ID）"
    exit 1
fi

# 构建请求体
BODY="{
  \"title\": \"$TITLE\",
  \"body\": \"$CONTENT\",
  \"public\": $PUBLIC
}"

if [[ -n "$SLUG" ]]; then
    BODY="{
  \"title\": \"$TITLE\",
  \"body\": \"$CONTENT\",
  \"public\": $PUBLIC,
  \"slug\": \"$SLUG\"
}"
fi

# 发送请求
echo "正在写入语雀..."
RESPONSE=$(curl -s -X POST \
    -H "X-Auth-Token: $YUQUE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$BODY" \
    "$YUQUE_API/repos/$REPO_ID/docs")

# 解析响应
if echo "$RESPONSE" | grep -q '"data"'; then
    DOC_URL=$(echo "$RESPONSE" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    DOC_TITLE=$(echo "$RESPONSE" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
    echo "✅ 文档创建成功！"
    echo "标题：$DOC_TITLE"
    echo "链接：https://www.yuque.com$DOC_URL"
else
    echo "❌ 文档创建失败"
    echo "响应：$RESPONSE"
    exit 1
fi
