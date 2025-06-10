#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MemotraceTimestampAlign - 从HTML文件中提取视频路径和时间戳，并修改视频文件的修改时间

使用说明：
1. 单文件模式：
   python update_video_mtime.py <html_file_path> [options]

2. 批量处理模式：
   python update_video_mtime.py -d <directory_path> [options]

参数：
  html_file_path              HTML文件路径（单文件模式，必需）
  -d, --directory PATH       包含多个聊天记录子文件夹的目录路径（批量模式）
  -b, --base-path PATH       视频文件基础路径（可选，默认为HTML文件所在目录）
  -v, --verbose              显示详细输出信息
  -h, --help                 显示帮助信息
"""

import os
import re
import datetime
import argparse
from pathlib import Path


def read_html_file(html_path):
    """读取HTML文件内容"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试其他编码
        try:
            with open(html_path, 'r', encoding='gbk') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(html_path, 'r', encoding='latin1') as f:
                return f.read()


def extract_video_timestamp_pairs(html_content):
    """从HTML内容中提取视频路径和时间戳对"""
    # 改进的正则表达式匹配模式
    # 支持两种格式：
    # 1. 传统格式: { type:43, text: './video/filename.mp4', timestamp:1514809949, ... }
    # 2. JSON格式: {"type": 43, "text": "./video/filename.mp4", "timestamp": 1514809949, ... }

    patterns = [
        # 传统格式（无引号包围属性名）- 匹配 type:43 和 .mp4 结尾的文件
        r'type\s*:\s*43[^}]*?text\s*:\s*["\']([^"\']+\.mp4)["\'][^}]*?timestamp\s*:\s*(\d+)',
        # JSON格式（有引号包围属性名和值）- 匹配 "type": 43 和 .mp4 结尾的文件
        r'"type"\s*:\s*43[^}]*?"text"\s*:\s*"([^"]+\.mp4)"[^}]*?"timestamp"\s*:\s*(\d+)',
    ]

    matches = []
    for pattern in patterns:
        found = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
        matches.extend(found)

    return matches


def timestamp_to_datetime(timestamp):
    """将时间戳转换为datetime对象"""
    return datetime.datetime.fromtimestamp(int(timestamp))


def set_file_modification_time(file_path, timestamp):
    """设置文件的修改时间"""
    if not os.path.exists(file_path):
        print(f"警告: 文件不存在 - {file_path}")
        return False

    try:
        # 将时间戳转换为文件系统时间
        mod_time = int(timestamp)
        os.utime(file_path, (mod_time, mod_time))
        return True
    except Exception as e:
        print(f"错误: 无法修改文件时间 {file_path} - {e}")
        return False


def process_html_file(html_path, base_path=None, verbose=False):
    """处理HTML文件，修改其中视频文件的时间戳"""
    html_path = Path(html_path)

    if not html_path.exists():
        print(f"错误: HTML文件不存在 - {html_path}")
        return    # 如果没有指定基础路径，使用HTML文件所在目录
    if base_path is None:
        base_path = html_path.parent
    else:
        base_path = Path(base_path)

    print(f"读取HTML文件: {html_path}")
    html_content = read_html_file(html_path)

    # 提取视频路径和时间戳对
    video_timestamp_pairs = extract_video_timestamp_pairs(html_content)

    if not video_timestamp_pairs:
        print("未找到匹配的视频文件和时间戳")
        return

    print(f"找到 {len(video_timestamp_pairs)} 个视频文件")

    success_count = 0
    total_count = len(video_timestamp_pairs)

    for video_path, timestamp in video_timestamp_pairs:
        # 构建完整的文件路径
        # 移除相对路径前缀 "./"
        relative_path = video_path.lstrip('./')
        full_path = base_path / relative_path

        # 转换时间戳为可读格式
        dt = timestamp_to_datetime(timestamp)

        print(f"\n处理文件: {relative_path}")
        print(f"时间戳: {timestamp} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")
        if verbose:
            print(f"完整路径: {full_path}")

        if set_file_modification_time(full_path, timestamp):
            print("✓ 成功修改文件时间")
            success_count += 1
        else:
            print("✗ 修改文件时间失败")

    print(f"\n处理完成: {success_count}/{total_count} 个文件成功修改")

    # 返回统计结果
    return {
        'total_found': total_count,
        'success_count': success_count,
        'failed_count': total_count - success_count
    }


def find_html_files_in_directory(directory_path):
    """在指定目录下查找所有子文件夹中的HTML文件"""
    directory_path = Path(directory_path)

    if not directory_path.exists():
        print(f"错误: 目录不存在 - {directory_path}")
        return []

    if not directory_path.is_dir():
        print(f"错误: 路径不是目录 - {directory_path}")
        return []

    html_files = []

    # 遍历所有子目录
    for subfolder in directory_path.iterdir():
        if subfolder.is_dir():
            # 在子目录中查找HTML文件
            for html_file in subfolder.glob("*.html"):
                html_files.append(html_file)

    return html_files


def process_directory_batch(directory_path, base_path=None, verbose=False):
    """批量处理目录下所有子文件夹中的HTML文件"""
    print(f"=== 批量处理模式 ===")
    print(f"扫描目录: {directory_path}")

    html_files = find_html_files_in_directory(directory_path)

    if not html_files:
        print("未找到任何HTML文件")
        return

    print(f"找到 {len(html_files)} 个HTML文件:")
    for html_file in html_files:
        print(f"  - {html_file}")

    print("\n" + "=" * 60)

    # 总体统计
    total_stats = {
        'processed_files': 0,
        'total_videos_found': 0,
        'total_videos_success': 0,
        'total_videos_failed': 0,
        'failed_html_files': []
    }

    # 逐个处理HTML文件
    for i, html_file in enumerate(html_files, 1):
        print(f"\n处理第 {i}/{len(html_files)} 个文件:")
        print(f"文件: {html_file.name}")
        print(f"路径: {html_file.parent}")
        print("-" * 40)

        try:
            result = process_html_file(html_file, base_path, verbose)

            if result:
                total_stats['processed_files'] += 1
                total_stats['total_videos_found'] += result['total_found']
                total_stats['total_videos_success'] += result['success_count']
                total_stats['total_videos_failed'] += result['failed_count']
            else:
                total_stats['failed_html_files'].append(html_file.name)

        except Exception as e:
            print(f"处理文件 {html_file.name} 时出错: {e}")
            total_stats['failed_html_files'].append(html_file.name)
            if verbose:
                import traceback
                traceback.print_exc()

        print("-" * 40)

    # 显示总体统计
    print("\n" + "=" * 60)
    print("【批量处理总体统计】")
    print(f"扫描到的HTML文件: {len(html_files)} 个")
    print(f"成功处理的HTML文件: {total_stats['processed_files']} 个")
    print(f"处理失败的HTML文件: {len(total_stats['failed_html_files'])} 个")

    if total_stats['failed_html_files']:
        print(f"失败的文件列表: {', '.join(total_stats['failed_html_files'])}")

    print(f"\n总共找到视频文件: {total_stats['total_videos_found']} 个")
    print(f"成功修改时间: {total_stats['total_videos_success']} 个")
    print(f"修改失败: {total_stats['total_videos_failed']} 个")

    if total_stats['total_videos_success'] == total_stats['total_videos_found'] and total_stats['total_videos_found'] > 0:
        print("✓ 所有视频文件时间戳修改完成！")
    elif total_stats['total_videos_success'] > 0:
        success_rate = (
            total_stats['total_videos_success'] / total_stats['total_videos_found']) * 100
        print(
            f"⚠ 部分完成：{total_stats['total_videos_success']}/{total_stats['total_videos_found']} 个文件修改成功 ({success_rate:.1f}%)")
    else:
        print("✗ 没有成功修改任何视频文件")

    print("=" * 60)

    return total_stats


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='从HTML文件中提取视频时间戳信息并修改视频文件的修改时间',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 单文件模式
  python update_video_mtime.py chat_export.html
  python update_video_mtime.py chat_export.html -b /path/to/videos -v
  python update_video_mtime.py "D:/WeChat/Export/chat.html" --verbose
  
  # 批量处理模式
  python update_video_mtime.py -d "F:/聊天记录"
  python update_video_mtime.py -d "F:/聊天记录" -v
  python update_video_mtime.py --directory "F:/聊天记录" --verbose
        """
    )

    # 创建互斥参数组，确保单文件模式和批量模式不能同时使用
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('html_file', nargs='?',
                       help='HTML文件路径（单文件模式）')

    group.add_argument('-d', '--directory',
                       dest='directory_path',
                       help='包含多个聊天记录子文件夹的目录路径（批量模式）')

    parser.add_argument('-b', '--base-path',
                        dest='base_path',
                        help='视频文件基础路径（默认使用HTML文件所在目录）')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='显示详细输出信息')

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    try:
        # 检查是否为批量处理模式
        if args.directory_path:
            # 批量处理模式
            if args.verbose:
                print("=== MemotraceTimestampAlign 视频时间戳同步工具 ===")
                print(f"批量处理目录: {args.directory_path}")
                if args.base_path:
                    print(f"自定义基础路径: {args.base_path}")
                print("=" * 50)

            process_directory_batch(
                args.directory_path, args.base_path, args.verbose)

        else:
            # 单文件处理模式
            if args.verbose:
                print("=== MemotraceTimestampAlign 视频时间戳同步工具 ===")
                print(f"HTML文件: {args.html_file}")
                if args.base_path:
                    print(f"基础路径: {args.base_path}")
                else:
                    print("基础路径: 使用HTML文件所在目录")
                print("=" * 50)

            result = process_html_file(
                args.html_file, args.base_path, args.verbose)

            # 显示最终统计信息
            if result:
                print("\n" + "=" * 50)
                print("【最终统计结果】")
                print(f"总共找到视频文件: {result['total_found']} 个")
                print(f"成功修改时间: {result['success_count']} 个")
                if result['failed_count'] > 0:
                    print(f"修改失败: {result['failed_count']} 个")

                if result['success_count'] == result['total_found']:
                    print("✓ 所有视频文件时间戳修改完成！")
                elif result['success_count'] > 0:
                    print(
                        f"⚠ 部分完成：{result['success_count']}/{result['total_found']} 个文件修改成功")
                else:
                    print("✗ 没有成功修改任何文件")
                print("=" * 50)

    except KeyboardInterrupt:
        print("\n操作被用户取消")
    except Exception as e:
        print(f"错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
