#!/bin/bash
# PUA 万能激励引擎执行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_FILE="$SCRIPT_DIR/motivation-templates.json"

# 解析参数
MODE=""
SCENARIO=""
TARGET=""
REASON=""
GOAL=""
CONTEXT=""
TONE="encouraging"

while [[ $# -gt 0 ]]; do
    case $1 in
        motivate)
            MODE="motivate"
            shift
            ;;
        comfort)
            MODE="comfort"
            shift
            ;;
        hype)
            MODE="hype"
            shift
            ;;
        custom)
            MODE="custom"
            shift
            ;;
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --reason)
            REASON="$2"
            shift 2
            ;;
        --goal)
            GOAL="$2"
            shift 2
            ;;
        --context)
            CONTEXT="$2"
            shift 2
            ;;
        --tone)
            TONE="$2"
            shift 2
            ;;
        *)
            echo "未知参数：$1"
            exit 1
            ;;
    esac
done

# 验证模板文件
if [[ ! -f "$TEMPLATES_FILE" ]]; then
    echo "错误：找不到模板文件 $TEMPLATES_FILE"
    exit 1
fi

# 输出头部
echo ""
echo "🔥 PUA 万能激励引擎 🔥"
echo ""

# 根据模式生成激励
case $MODE in
    motivate)
        if [[ -z "$SCENARIO" ]]; then
            SCENARIO="general"
        fi
        echo "【${SCENARIO^}场景${TARGET:+ - 给$TARGET}】"
        echo ""
        # 随机选择一条激励语
        QUOTES=$(jq -r ".scenarios.${SCENARIO}.${TONE}[]" "$TEMPLATES_FILE" 2>/dev/null || echo "")
        if [[ -n "$QUOTES" ]]; then
            echo "$QUOTES" | shuf -n 1
        else
            echo "你比你自己想象的更强大。相信自己，你能做到的远不止于此！"
        fi
        echo ""
        ;;
    comfort)
        echo "【安慰模式 - ${REASON:-遇到困难}】"
        echo ""
        REASON_KEY="failure"
        [[ "$REASON" == *"拒绝"* ]] && REASON_KEY="rejection"
        [[ "$REASON" == *"压力"* ]] && REASON_KEY="stress"
        [[ "$REASON" == *"失去"* || "$REASON" == *"分手"* ]] && REASON_KEY="loss"
        
        QUOTES=$(jq -r ".comfort_templates.${REASON_KEY}[]" "$TEMPLATES_FILE" 2>/dev/null || echo "")
        if [[ -n "$QUOTES" ]]; then
            echo "$QUOTES" | shuf -n 1
        else
            echo "你已经做得很好了，别对自己太苛刻。慢慢来，一切都会好的。"
        fi
        echo ""
        ;;
    hype)
        echo "【打鸡血模式 - ${GOAL:-目标}】"
        echo ""
        QUOTES=$(jq -r ".hype_templates[]" "$TEMPLATES_FILE" 2>/dev/null || echo "")
        if [[ -n "$QUOTES" ]]; then
            echo "$QUOTES" | shuf -n 1
        else
            echo "🔥 燃起来！今天就是你的转折点，从这一刻开始，你就是那个传奇！"
        fi
        echo ""
        ;;
    custom)
        echo "【自定义场景 - ${CONTEXT:-当前情况}】"
        echo ""
        echo " tone: ${TONE}"
        echo ""
        # 使用通用模板
        QUOTES=$(jq -r ".scenarios.general.${TONE}[]" "$TEMPLATES_FILE" 2>/dev/null || echo "")
        if [[ -n "$QUOTES" ]]; then
            echo "$QUOTES" | shuf -n 1
        else
            echo "你现在的每一分努力，都是在为将来的自己铺路。别放弃！"
        fi
        echo ""
        ;;
    *)
        echo "用法："
        echo "  $0 motivate --scenario work --target 同事 --tone encouraging"
        echo "  $0 comfort --reason 项目失败"
        echo "  $0 hype --goal 完成 KPI"
        echo "  $0 custom --context 明天要演讲 --tone gentle"
        echo ""
        exit 1
        ;;
esac

echo "—— 来自 蜡笔小猪的激励 🐷"
echo ""
