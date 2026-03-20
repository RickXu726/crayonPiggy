# 语雀写入技能 (yuque-writer)

## 功能

将文档、笔记等内容写入语雀知识库。

## 配置

在 `TOOLS.md` 中添加语雀配置：

```markdown
### 语雀

- API Token: `<your-yuque-token>`
- 默认知识库 ID: `<optional-default-repo-id>`
```

## 使用方式

### 1. 创建/更新文档

```bash
# 基本用法
openclaw skill yuque-writer write --title "文档标题" --content "文档内容" --repo-id <知识库 ID>

# 更新已有文档
openclaw skill yuque-writer write --title "文档标题" --content "文档内容" --repo-id <知识库 ID> --slug <文档 slug>
```

### 2. 创建知识库

```bash
openclaw skill yuque-writer create-repo --name "知识库名称" --description "知识库描述"
```

### 3. 列出知识库

```bash
openclaw skill yuque-writer list-repos
```

## 参数说明

| 参数 | 说明 | 必填 |
|-----|------|-----|
| `--title` | 文档标题 | 是 |
| `--content` | 文档内容（支持 Markdown） | 是 |
| `--repo-id` | 知识库 ID | 是（除非配置了默认） |
| `--slug` | 文档 slug（用于更新） | 否 |
| `--public` | 是否公开文档 | 否，默认 0（私有） |

## API 参考

语雀 API 文档：https://www.yuque.com/yuque/developer

## 注意事项

1. API Token 需要妥善保管，不要提交到 git
2. 文档内容支持 Markdown 格式
3. 首次使用需要在语雀生成 API Token
