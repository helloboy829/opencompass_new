"""
检查修改记录是否更新的脚本

使用方法：
    python tools/check_changelog.py
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def check_changelog():
    """检查 CHANGELOG_CUSTOM.md 是否最近更新过"""

    changelog_path = Path('CHANGELOG_CUSTOM.md')

    if not changelog_path.exists():
        print("❌ 错误：找不到 CHANGELOG_CUSTOM.md 文件")
        print("   请确保在项目根目录运行此脚本")
        return False

    # 获取文件最后修改时间
    mtime = os.path.getmtime(changelog_path)
    last_modified = datetime.fromtimestamp(mtime)
    now = datetime.now()

    # 计算时间差
    time_diff = now - last_modified

    print("=" * 60)
    print("修改记录检查")
    print("=" * 60)
    print(f"文件路径: {changelog_path.absolute()}")
    print(f"最后更新: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"距今时间: {format_timedelta(time_diff)}")
    print("=" * 60)

    # 读取最新的修改日期
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找最新的修改日期
    import re
    dates = re.findall(r'## 修改日期：(\d{4}-\d{2}-\d{2})', content)

    if dates:
        latest_date = dates[0]
        print(f"\n最新记录日期: {latest_date}")

        # 检查是否是今天
        today = datetime.now().strftime('%Y-%m-%d')
        if latest_date == today:
            print("✅ 状态：今天已更新修改记录")
            return True
        else:
            print("⚠️  状态：修改记录不是今天的")
            print(f"   最新记录是 {latest_date}，今天是 {today}")
            return False
    else:
        print("⚠️  警告：未找到修改日期记录")
        return False


def format_timedelta(td):
    """格式化时间差"""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days} 天")
    if hours > 0:
        parts.append(f"{hours} 小时")
    if minutes > 0:
        parts.append(f"{minutes} 分钟")
    if not parts:
        parts.append(f"{seconds} 秒")

    return " ".join(parts)


def show_recent_changes():
    """显示最近的修改记录"""
    changelog_path = Path('CHANGELOG_CUSTOM.md')

    if not changelog_path.exists():
        return

    print("\n" + "=" * 60)
    print("最近的修改记录（前 30 行）")
    print("=" * 60)

    with open(changelog_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:30], 1):
            print(line.rstrip())

    if len(lines) > 30:
        print(f"\n... 还有 {len(lines) - 30} 行")


def main():
    print("\n🔍 检查项目修改记录\n")

    result = check_changelog()

    if not result:
        print("\n" + "=" * 60)
        print("💡 提醒")
        print("=" * 60)
        print("如果你最近修改了项目文件，请更新 CHANGELOG_CUSTOM.md")
        print("\n参考文档：")
        print("  - REMINDER_CHANGELOG.md（修改记录规范）")
        print("  - CHANGELOG_CUSTOM.md（修改记录文件）")
        print("=" * 60)

    # 显示最近的修改
    show_recent_changes()

    return result


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
