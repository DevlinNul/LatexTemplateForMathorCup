#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import glob
import sys


def strip_quotes(s):
    """去除字符串首尾匹配的引号（单引号或双引号）"""
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def replace_tex_commands(tex_file):
    """在 tex 文件中替换 section 相关命令"""
    try:
        with open(tex_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 执行替换
        content = content.replace("\\section", "\\additionalSection")
        content = content.replace("\\subsection", "\\additionalSubsection")
        content = content.replace("\\subsubsection", "\\additionalSubsubsection")

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"已替换命令: {tex_file}")
    except Exception as e:
        print(f"替换命令时出错 {tex_file}: {e}")


def convert_md_to_tex(md_file):
    """使用 pandoc 将 md 文件转换为同名的 tex 文件"""
    base_name = os.path.splitext(md_file)[0]  # 去掉扩展名
    tex_file = base_name + ".tex"

    cmd = [
        "pandoc",
        md_file,
        "-o",
        tex_file,
        "--from",
        "markdown+tex_math_single_backslash+raw_tex",
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"转换成功: {md_file} -> {tex_file}")
        return tex_file
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {md_file}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
        return None
    except FileNotFoundError:
        print("错误: 未找到 pandoc，请确保已安装 pandoc 并已添加到 PATH 环境变量。")
        sys.exit(1)


def main():
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"当前工作目录: \"{os.getcwd()}\"")

    # 获取用户输入
    src = input(
        "请输入 md 文件的路径（记得带后缀名），支持使用 * 指代脚本所在目录下的所有 md 文件: "
    ).strip()

    # 去除可能存在的首尾引号
    src = strip_quotes(src)

    # 确定待处理的 md 文件列表
    if src == "*":
        md_files = glob.glob("*.md")
        if not md_files:
            print("当前目录下没有找到任何 .md 文件。")
            return
        print(f"找到 {len(md_files)} 个 md 文件，开始处理...")
    else:
        # 单个文件路径
        if not os.path.isfile(src):
            print(f"错误: 文件 '{src}' 不存在。")
            return
        md_files = [src]

    # 处理每个 md 文件
    for md_file in md_files:
        tex_file = convert_md_to_tex(md_file)
        if tex_file:
            replace_tex_commands(tex_file)

    print("所有任务完成。")


if __name__ == "__main__":
    main()