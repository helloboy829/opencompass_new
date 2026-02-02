# 🔔 重要提醒：修改记录规范

## ⚠️ 每次修改项目文件后，必须更新修改记录！

### 📝 修改记录文件位置
```
CHANGELOG_CUSTOM.md
```

---

## 📋 修改记录模板

每次修改后，在 `CHANGELOG_CUSTOM.md` 文件顶部添加新的修改记录：

```markdown
## 修改日期：YYYY-MM-DD

### 📋 修改目的
[简要说明本次修改的目的]

---

## 🆕 新增文件
- **文件**: `路径/文件名`
- **说明**: [文件用途]
- **功能**: [主要功能列表]

## 📝 修改文件
- **文件**: `路径/文件名`
- **修改内容**: [具体修改了什么]
- **原因**: [为什么要修改]

## 🗑️ 删除文件
- **文件**: `路径/文件名`
- **原因**: [为什么删除]

---

## 🔧 配置变更
[列出配置参数的变更]

## 🚀 使用方法变更
[如果使用方法有变化，说明新的使用方法]

## 📖 文档更新
[列出更新的文档]

---

**修改完成时间**: YYYY-MM-DD HH:MM
**修改人**: [你的名字或 AI]
**版本**: vX.X

---
```

---

## 🤖 如何让 AI 记住更新修改记录

### 方法 1：在项目根目录创建提醒文件（推荐）

创建文件：`.ai-reminder.md` 或 `AI_INSTRUCTIONS.md`

内容：
```markdown
# AI 助手必读指令

## 🔴 强制规则：每次修改后必须更新 CHANGELOG_CUSTOM.md

无论进行任何文件的增删改操作，都必须：

1. 在完成修改后，立即更新 `CHANGELOG_CUSTOM.md`
2. 在文件顶部添加新的修改记录
3. 记录所有新增、修改、删除的文件
4. 说明修改目的和影响

## 📝 修改记录检查清单

- [ ] 记录了所有新增的文件
- [ ] 记录了所有修改的文件
- [ ] 记录了所有删除的文件
- [ ] 说明了修改目的
- [ ] 更新了使用方法（如有变化）
- [ ] 添加了时间戳和版本号

## ⚠️ 如果忘记更新

用户会在每次对话开始时提醒：
"请先检查上次修改是否已记录到 CHANGELOG_CUSTOM.md"
```

### 方法 2：在每次对话开始时提醒 AI

在每次新对话开始时，先发送：

```
请先检查 CHANGELOG_CUSTOM.md，确保上次的修改已经记录。
然后再开始新的任务。
```

### 方法 3：使用 Git Hook（自动化）

创建 `.git/hooks/pre-commit` 文件：

```bash
#!/bin/bash

# 检查是否有文件修改
if git diff --cached --name-only | grep -v "CHANGELOG_CUSTOM.md" > /dev/null; then
    # 检查 CHANGELOG_CUSTOM.md 是否也被修改
    if ! git diff --cached --name-only | grep "CHANGELOG_CUSTOM.md" > /dev/null; then
        echo "⚠️  警告：你修改了文件但没有更新 CHANGELOG_CUSTOM.md"
        echo "请更新修改记录后再提交！"
        exit 1
    fi
fi
```

### 方法 4：在 IDE 中设置提醒

如果使用 VS Code，创建 `.vscode/tasks.json`：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "提醒更新修改记录",
            "type": "shell",
            "command": "echo",
            "args": ["⚠️  记得更新 CHANGELOG_CUSTOM.md！"],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "runOptions": {
                "runOn": "folderOpen"
            }
        }
    ]
}
```

---

## 🎯 最佳实践

### 对于用户（你）

1. **每次对话开始时**，先问 AI：
   ```
   上次的修改是否已记录到 CHANGELOG_CUSTOM.md？
   ```

2. **每次对话结束时**，要求 AI：
   ```
   请总结本次对话的所有修改，并更新 CHANGELOG_CUSTOM.md
   ```

3. **定期检查**：
   ```bash
   git log --oneline CHANGELOG_CUSTOM.md
   ```

### 对于 AI

1. **每次修改文件后**，主动询问：
   ```
   我已完成修改，是否需要我更新 CHANGELOG_CUSTOM.md？
   ```

2. **对话结束前**，主动提醒：
   ```
   本次对话修改了 X 个文件，我已更新 CHANGELOG_CUSTOM.md
   ```

---

## 📌 快速命令

### 查看最近的修改记录
```bash
head -n 50 CHANGELOG_CUSTOM.md
```

### 查看所有修改日期
```bash
grep "## 修改日期" CHANGELOG_CUSTOM.md
```

### 统计修改次数
```bash
grep -c "## 修改日期" CHANGELOG_CUSTOM.md
```

---

## 🔗 相关文件

- **修改记录**: `CHANGELOG_CUSTOM.md`
- **提醒文件**: `REMINDER_CHANGELOG.md`（本文件）
- **使用指南**: `docs/custom_supergpqa_guide.md`
- **快速参考**: `README_QUICKSTART.md`

---

## 💡 提示

将此文件内容复制到每次对话的开头，或者在 IDE 中置顶显示，
这样每次开始工作时都能看到提醒！

---

**创建时间**: 2026-02-02
**用途**: 确保项目修改记录的完整性和可追溯性
