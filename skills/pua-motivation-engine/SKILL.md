# PUA 万能激励引擎 (pua-motivation-engine)

## 功能

生成各种场景下的激励话术，用 PUA 式的方式给人打鸡血、鼓励、安慰。

**注意**：这里是正能量的"PUA"，不是贬义的操控术～ 是那种让人听了就想站起来奋斗的激励！

## 使用方式

```bash
# 基础激励
openclaw skill pua-motivation-engine motivate --scenario "work" --target "同事"

# 安慰模式
openclaw skill pua-motivation-engine comfort --reason "项目失败"

# 打鸡血模式
openclaw skill pua-motivation-engine hype --goal "完成 KPI"

# 自定义场景
openclaw skill pua-motivation-engine custom --context "明天要演讲" --tone "encouraging"
```

## 场景参数

| 场景 | 说明 |
|-----|------|
| `work` | 工作场景 |
| `study` | 学习/考试 |
| `fitness` | 健身/减肥 |
| `relationship` | 感情问题 |
| `career` | 职业发展 |
| `startup` | 创业 |
| `general` | 通用场景 |

## 语气参数

| 语气 | 说明 |
|-----|------|
| `encouraging` | 鼓励型 |
| `aggressive` | 激进型（打鸡血） |
| `gentle` | 温柔型（安慰） |
| `humorous` | 幽默型 |
| `philosophical` | 哲理型 |

## 输出示例

```
🔥 PUA 万能激励引擎 🔥

【工作场景 - 给同事】

"你知道为什么你比那些人厉害吗？因为你还在努力，而他们已经在躺平了！
这个项目就是你的机会，抓住了，你就是下一个被挖角的！
别跟我说什么不可能，你之前搞定的那个 XX 项目，当时谁说能成的？
相信自己，你比你想象的更强！"

—— 来自 蜡笔小猪的激励 🐷
```

## 注意事项

1. 本技能仅用于正能量激励，不用于情感操控
2. 可根据对方性格调整语气强度
3. 建议配合实际行动支持，不要光说不做

## 扩展

可以在 `motivation-templates.json` 中添加自定义模板。
