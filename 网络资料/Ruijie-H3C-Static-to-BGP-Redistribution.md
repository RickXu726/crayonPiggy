# Ruijie & H3C 静态路由重分布到 BGP 配置指南

> 文档版本：1.0  
> 创建日期：2026-03-20  
> 作者：蜡笔小猪 🐷

---

## 核心原则

**静态路由优先级必须低于 BGP 路由优先级**，确保 BGP 路由优选。

| 设备厂商 | 静态路由默认优先级 | BGP 路由优先级 | 调整后静态路由优先级 |
|---------|------------------|--------------|-------------------|
| H3C     | 60               | 255 (IBGP/EBGP) | >255 (建议 200) |
| Ruijie  | 1 (管理距离)      | EBGP 20 / IBGP 200 | >200 (建议 210) |

---

## H3C 设备配置

### 1. 基础 BGP 配置

```bash
# 进入 BGP 视图
bgp <AS-number>

# 配置路由器 ID
router-id <x.x.x.x>

# 配置 BGP 对等体
peer <neighbor-ip> as-number <AS-number>
peer <neighbor-ip> connect-interface <interface-name>

# 激活对等体
peer <neighbor-ip> enable
```

### 2. 静态路由重分布到 BGP

```bash
# 方法一：network 方式宣告（推荐）
bgp <AS-number>
 network <network-address> <mask>

# 方法二：import-route 重分布
bgp <AS-number>
 import-route static route-policy STATIC-TO-BGP
```

### 3. 路由策略配置（关键）

```bash
# 创建 ACL 匹配静态路由
acl number 2000
 rule 5 permit source <network-address> <wildcard-mask>

# 创建 Route-Policy
route-policy STATIC-TO-BGP permit node 10
 if-match acl 2000
 apply cost 200          # MED 值，越大优先级越低
 apply local-preference 50  # Local Pref，越小优先级越低
 apply as-path 65000 65000 additive  # 增加 AS-Path 长度
 apply community 65000:100  # 添加 Community 标记

# 应用 Route-Policy
bgp <AS-number>
 import-route static route-policy STATIC-TO-BGP
```

### 4. 完整配置示例

```bash
sysname H3C-Router

# 配置静态路由
ip route-static 10.1.0.0 255.255.0.0 192.168.1.1
ip route-static 10.2.0.0 255.255.0.0 192.168.1.1

# 配置 ACL
acl number 2000
 rule 5 permit source 10.1.0.0 0.0.255.255
 rule 10 permit source 10.2.0.0 0.0.255.255

# 配置 Route-Policy
route-policy STATIC-TO-BGP permit node 10
 if-match acl 2000
 apply cost 200
 apply local-preference 50
 apply as-path 65000 65000 additive
 apply community 65000:100

route-policy STATIC-TO-BGP permit node 20

# 配置 BGP
bgp 65000
 router-id 1.1.1.1
 peer 192.168.100.1 as-number 65001
 peer 192.168.100.1 connect-interface GigabitEthernet1/0/1
 peer 192.168.100.1 enable
 import-route static route-policy STATIC-TO-BGP
```

### 5. 验证命令

```bash
# 查看 BGP 路由表
display bgp routing-table

# 查看 BGP 对等体状态
display bgp peer

# 查看 Route-Policy
display route-policy STATIC-TO-BGP

# 查看路由优先级
display ip routing-table protocol bgp
display ip routing-table protocol static
```

---

## Ruijie 设备配置

### 1. 基础 BGP 配置

```bash
# 启用 BGP 路由进程
router bgp <AS-number>

# 配置路由器 ID
bgp router-id <x.x.x.x>

# 配置 BGP 邻居
neighbor <neighbor-ip> remote-as <AS-number>
neighbor <neighbor-ip> update-source <interface-name>
```

### 2. 静态路由重分布到 BGP

```bash
# 方法一：network 方式宣告（推荐）
router bgp <AS-number>
 network <network-address> mask <subnet-mask>

# 方法二：redistribute 重分布
router bgp <AS-number>
 redistribute static route-map STATIC-TO-BGP
```

### 3. 路由映射配置（关键）

```bash
# 创建 ACL 匹配静态路由
ip access-list standard STATIC-ROUTES
 permit <network-address> <wildcard-mask>

# 创建 Route-Map
route-map STATIC-TO-BGP permit 10
 match ip address STATIC-ROUTES
 set metric 200           # MED 值
 set local-preference 50  # Local Pref
 set as-path prepend 65000 65000  # 增加 AS-Path
 set community 65000:100  # Community

# 允许其他路由通过
route-map STATIC-TO-BGP permit 20
```

### 4. 完整配置示例

```bash
hostname Ruijie-Router

# 配置静态路由
ip route 10.1.0.0 255.255.0.0 192.168.1.1
ip route 10.2.0.0 255.255.0.0 192.168.1.1

# 配置 ACL
ip access-list standard STATIC-ROUTES
 permit 10.1.0.0 0.0.255.255
 permit 10.2.0.0 0.0.255.255

# 配置 Route-Map
route-map STATIC-TO-BGP permit 10
 match ip address STATIC-ROUTES
 set metric 200
 set local-preference 50
 set as-path prepend 65000 65000
 set community 65000:100

route-map STATIC-TO-BGP permit 20

# 配置 BGP
router bgp 65000
 bgp router-id 1.1.1.1
 neighbor 192.168.100.1 remote-as 65001
 neighbor 192.168.100.1 update-source GigabitEthernet0/1
 redistribute static route-map STATIC-TO-BGP
```

### 5. 验证命令

```bash
# 查看 BGP 路由表
show ip bgp

# 查看 BGP 邻居状态
show ip bgp summary

# 查看 Route-Map
show route-map STATIC-TO-BGP

# 查看路由表
show ip route bgp
show ip route static
```

---

## 路由属性调整说明

### 关键属性优先级对比

| 属性 | H3C 命令 | Ruijie 命令 | 说明 | 建议值 |
|-----|---------|------------|------|--------|
| MED/Cost | `apply cost` | `set metric` | 越小越优先 | 200+ |
| Local Preference | `apply local-preference` | `set local-preference` | 越大越优先 | 50-80 |
| AS-Path | `apply as-path ... additive` | `set as-path prepend` | 越短越优先 | prepend 2-3 次 |
| Community | `apply community` | `set community` | 标记用途 | 自定义 |
| Weight (仅本地) | - | `set weight` | 越大越优先 | 不设置 (默认 0) |

### 为什么静态路由属性要更低？

1. **BGP 选路规则**：BGP 有复杂的选路算法，默认优先选择：
   - Weight 最大（Ruijie/Cisco）
   - Local Preference 最大
   - 本地起源
   - AS-Path 最短
   - MED 最小

2. **避免路由环路**：如果静态路由优先级高于 BGP，可能导致：
   - BGP 学习到的路由不被优选
   - 路由黑洞
   - 次优路径

3. **网络稳定性**：BGP 路由通常经过路径优选，比静态路由更可靠

---

## 常见问题排查

### 1. 路由未重分布

```bash
# H3C
display bgp routing-table static  # 查看静态路由是否进入 BGP

# Ruijie
show ip bgp static  # 查看静态路由是否进入 BGP
```

**解决方案**：检查 Route-Policy/Route-Map 是否正确匹配

### 2. 路由属性未生效

```bash
# H3C
display bgp routing-table <network>  # 查看具体路由属性

# Ruijie
show ip bgp <network>  # 查看具体路由属性
```

**解决方案**：确认 apply/set 命令在正确的 node/sequence 中

### 3. 邻居关系未建立

```bash
# H3C
display bgp peer  # 查看邻居状态

# Ruijie
show ip bgp summary  # 查看邻居摘要
```

**解决方案**：检查 TCP 179 端口、AS 号、Router-ID 是否冲突

---

## 最佳实践建议

1. **优先使用 network 宣告**：比 import-route/redistribute 更可控
2. **配置路由过滤**：避免意外宣告敏感路由
3. **添加 Community 标记**：便于后续策略调整
4. **定期验证**：确保重分布按预期工作
5. **文档化**：记录所有 Route-Policy/Route-Map 的用途

---

## 参考文档

- H3C 官方文档：BGP 配置指南
- Ruijie 官方文档：BGP 配置手册
- RFC 4271: A Border Gateway Protocol 4 (BGP-4)

---

_文档由 蜡笔小猪 🐷 整理完成_
