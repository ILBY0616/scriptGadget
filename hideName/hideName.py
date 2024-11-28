import os
import string


# 功能：隐藏指定目录下所有快捷方式文件的名称
# 实现原理：
# 1. 获取目录下的所有快捷方式文件（后缀为 .lnk）。
# 2. 遍历文件，将名称改为仅由空格组成的文件名。
# 3. 如果空格命名冲突，则使用字母命名作为备用。
# 4. 使用集合追踪当前目录中所有文件名，避免命名重复。

def hide_shortcut_names(directory):
    # 获取目录中所有快捷方式文件（后缀为 .lnk）
    shortcuts = [f for f in os.listdir(directory) if f.endswith('.lnk')]

    # 用于记录当前目录中的文件名，避免命名冲突
    existing_files = set(shortcuts)

    for index, shortcut in enumerate(shortcuts):
        spaces = None  # 用于存储新的文件名（空格或字母）

        # 尝试生成唯一的空格文件名
        for i in range(1, len(shortcuts) + 1):
            candidate = f"{' ' * i}.lnk"
            if candidate not in existing_files:
                spaces = ' ' * i
                break

        # 如果空格文件名都被占用，使用字母命名
        if spaces is None:
            spaces = string.ascii_letters[index % len(string.ascii_letters)]

        # 生成新文件名并构造完整路径
        new_name = f"{spaces}.lnk"
        old_path = os.path.join(directory, shortcut)
        new_path = os.path.join(directory, new_name)

        try:
            # 重命名文件
            os.rename(old_path, new_path)
            # 更新已存在文件集合
            existing_files.add(new_name)
            print(f"已隐藏名称: {shortcut} -> {new_name}")
        except Exception as e:
            # 捕获重命名过程中出现的错误
            print(f"重命名失败: {shortcut}，错误: {e}")


if __name__ == "__main__":
    # 获取桌面路径（支持多语言环境的 Windows 系统）
    desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")

    # 输出桌面路径，便于调试
    print("桌面路径:", desktop)

    # 检查桌面路径是否有效
    if os.path.exists(desktop) and os.path.isdir(desktop):
        hide_shortcut_names(desktop)
        print("桌面快捷方式名称已隐藏！")
    else:
        print("桌面路径无效，请检查系统设置！")
