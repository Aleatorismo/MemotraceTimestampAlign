# MemotraceTimestampAlign

此项目旨在解决 Memotrace 软件导出微信聊天记录时视频文件时间戳不准确的问题。通过读取 Memotrace 生成的 HTML 文件，提取其中记录的正确时间戳，并据此更新对应视频文件的修改日期，从而确保视频文件的日期与其实际发送日期一致。

## 功能特点

- 解析HTML文件中的视频路径和时间戳信息
- 支持两种数据格式：传统格式和JSON格式
- 自动匹配形如 `{ type:43, text: './video/xxx.mp4', timestamp:1514809949, ... }` 的数据片段
- 支持新的JSON格式：`{"type": 43, "text": "./video/2024-01/filename.mp4", "timestamp": 1514809949, ...}`
- 将Unix时间戳转换为标准日期时间格式
- **支持单文件和批量处理两种模式**
- 支持多种文本编码格式（UTF-8、GBK、Latin1）
- 命令行参数模式，灵活易用
- 详细的处理日志和错误报告
- 完整的统计信息显示（总数、成功数、失败数）

## 使用方法

### 单文件处理模式

#### 基本用法
```bash
python update_video_mtime.py <html_file_path>
```

#### 指定视频文件基础路径
```bash
python update_video_mtime.py <html_file_path> -b <video_base_path>
```

#### 详细输出模式
```bash
python update_video_mtime.py <html_file_path> -v
```

#### 组合使用
```bash
python update_video_mtime.py chat_export.html -b D:\WeChat\Videos -v
```

### 批量处理模式

#### 基本用法
```bash
python update_video_mtime.py -d <directory_path>
```

#### 详细输出模式
```bash
python update_video_mtime.py -d <directory_path> -v
```

#### 指定自定义基础路径
```bash
python update_video_mtime.py -d <directory_path> -b <custom_base_path> -v
```

## 参数说明

### 互斥参数组（必须选择其一）
- `html_file`: HTML文件路径（单文件模式）
- `-d, --directory`: 包含多个聊天记录子文件夹的目录路径（批量模式）

### 可选参数
- `-b, --base-path`: 视频文件基础路径（可选，默认为HTML文件或各子文件夹所在目录）
- `-v, --verbose`: 详细输出模式（可选）
- `-h, --help`: 显示帮助信息

## 使用场景

### 单文件处理
适用于处理单个HTML文件的情况：
```
chat_export.html      # 要处理的HTML文件
video/               # 包含视频文件的目录
  ├── video1.mp4
  ├── video2.mp4
  └── ...
```

### 批量处理
适用于有多个聊天记录的情况，每个子文件夹包含一个聊天记录：
```
F:\聊天记录\           # 主目录
├── 张三\              # 子文件夹1
│   ├── chat.html     # HTML聊天记录
│   └── video\        # 视频目录
│       ├── video1.mp4
│       └── video2.mp4
├── 李四\              # 子文件夹2
│   ├── export.html   # HTML聊天记录
│   └── video\        # 视频目录
│       └── video3.mp4
└── 群聊ABC\           # 子文件夹3
    ├── group_chat.html
    └── video\
        ├── video4.mp4
        └── video5.mp4
```

## 示例

### 单文件处理示例

假设你有一个名为 `chat_export.html` 的文件，位于当前目录，其中包含视频时间戳信息：

#### 1. 基本使用（视频文件与HTML文件在同一目录）
```bash
python update_video_mtime.py chat_export.html
```

#### 2. 指定视频文件目录
```bash
python update_video_mtime.py chat_export.html -b D:\WeChat\Videos
```

#### 3. 详细输出模式
```bash
python update_video_mtime.py chat_export.html -v
```

#### 4. 使用绝对路径
```bash
python update_video_mtime.py "D:\WeChat\Export\chat.html" --verbose
```

### 批量处理示例

假设你有多个聊天记录文件夹，每个文件夹都包含HTML文件和对应的video目录：

#### 1. 基本批量处理
```bash
python update_video_mtime.py -d "F:\聊天记录"
```

#### 2. 批量处理 + 详细输出
```bash
python update_video_mtime.py -d "F:\聊天记录" -v
```

#### 3. 批量处理 + 自定义基础路径
```bash
python update_video_mtime.py -d "F:\聊天记录" -b "G:\备份视频" -v
```

### 典型输出示例

#### 单文件处理输出：
```
=== MemotraceTimestampAlign 视频时间戳同步工具 ===
HTML文件: chat_export.html
基础路径: 使用HTML文件所在目录
==================================================

=== 处理HTML文件: chat_export.html ===
✓ 成功读取HTML文件
✓ 成功提取数据：找到 5 个视频条目

正在处理视频文件...

处理文件: video1.mp4
路径: ./video/video1.mp4
时间戳: 1514809949 (2018-01-01 18:45:49)
✓ 成功修改文件时间

处理文件: video2.mp4
路径: ./video/video2.mp4
时间戳: 1514810123 (2018-01-01 18:48:43)
✓ 成功修改文件时间

处理完成: 5/5 个文件成功修改

==================================================
【最终统计结果】
总共找到视频文件: 5 个
成功修改时间: 5 个
✓ 所有视频文件时间戳修改完成！
==================================================
```

#### 批量处理输出：
```
=== MemotraceTimestampAlign 视频时间戳同步工具 ===
批量处理目录: F:\聊天记录
==================================================

=== 批量处理模式 ===
扫描目录: F:\聊天记录
找到 3 个HTML文件:
  - F:\聊天记录\张三\chat.html
  - F:\聊天记录\李四\export.html
  - F:\聊天记录\群聊ABC\group_chat.html

============================================================

处理第 1/3 个文件:
文件: chat.html
路径: F:\聊天记录\张三
----------------------------------------
... (详细处理过程)
处理完成: 3/3 个文件成功修改

处理第 2/3 个文件:
文件: export.html
路径: F:\聊天记录\李四
----------------------------------------
... (详细处理过程)
处理完成: 2/2 个文件成功修改

处理第 3/3 个文件:
文件: group_chat.html
路径: F:\聊天记录\群聊ABC
----------------------------------------
... (详细处理过程)
处理完成: 8/8 个文件成功修改

============================================================
【批量处理总体统计】
扫描到的HTML文件: 3 个
成功处理的HTML文件: 3 个
处理失败的HTML文件: 0 个

总共找到视频文件: 13 个
成功修改时间: 13 个
修改失败: 0 个
✓ 所有视频文件时间戳修改完成！
============================================================
```

```bash
python update_video_mtime.py chat_export.html -v
```

#### 4. 完整示例（包含所有参数）

```bash
python update_video_mtime.py "D:\WeChat\Export\chat.html" -b "D:\WeChat\Videos" -v
```

### HTML文件内容示例

脚本能够识别以下两种格式的数据：

#### 1. 传统格式（无引号包围属性名）
```javascript
{ type:43, text: './video/c22b1e03cd045cadb20f1aea18cad327.mp4',MsgSvrID:6923580432799902227,is_send:0,avatar_path:'1',timestamp:1514809949,is_chatroom:1,displayname:'郑福胜'}
```

#### 2. JSON格式（有引号包围属性名，支持子目录）
```javascript
{"type": 43, "text": "./video/2024-01/20240125075621.mp4", "MsgSvrID": "1812312321483237439", "is_send": 0, "avatar_path": 2, "timestamp": 1706140581, "is_chatroom": 1, "displayname": "郑福胜", "token": "e323c70717d6e9352459cff00031098e"}
```

**支持的路径格式：**
- 简单路径：`./video/filename.mp4`
- 带子目录：`./video/2024-01/filename.mp4`
- 多级子目录：`./video/2024/01/filename.mp4`

### 运行结果示例

```
=== MemotraceTimestampAlign 视频时间戳同步工具 ===
HTML文件: chat_export.html
基础路径: 使用HTML文件所在目录
==================================================

读取HTML文件: chat_export.html
找到 1 个视频文件

处理文件: video/c22b1e03cd045cadb20f1aea18cad327.mp4
时间戳: 1514809949 (2018-01-01 20:32:29)
完整路径: D:\WeChat\Export\video\c22b1e03cd045cadb20f1aea18cad327.mp4
✓ 成功修改文件时间

处理完成: 1/1 个文件成功修改

==================================================
【最终统计结果】
总共找到视频文件: 1 个
成功修改时间: 1 个
✓ 所有视频文件时间戳修改完成！
==================================================
```

## 工作流程

脚本运行时会执行以下步骤：

1. **读取HTML文件**：使用多种编码格式尝试读取HTML文件内容
2. **提取数据**：使用正则表达式匹配包含 `./video/` 路径和 `timestamp` 的数据块
3. **路径解析**：构建视频文件的完整路径
4. **时间转换**：将Unix时间戳转换为系统文件时间格式
5. **修改时间**：更新视频文件的修改时间
6. **统计报告**：显示处理结果和统计信息

## 注意事项

- **文件路径**：确保HTML文件路径配置正确，支持绝对路径和相对路径
- **视频文件存在性**：脚本会检查视频文件是否存在，不存在的文件会显示警告
- **权限要求**：需要对视频文件有写入权限才能修改文件时间
- **备份建议**：建议在运行脚本前备份重要的视频文件
- **路径格式**：脚本支持Windows和Unix风格的路径分隔符

## 故障排除

### 常见问题

#### 1. "未找到匹配的视频文件和时间戳"
**原因：** HTML文件中没有符合格式的视频数据
**解决方法：**
- 检查HTML文件是否为Memotrace导出的文件
- 确认HTML文件中包含 `type: 43` 或 `"type": 43` 的视频消息
- 验证路径格式是否正确（应包含 `./video/` 前缀）

#### 2. "警告: 文件不存在"
**原因：** 视频文件路径不正确或文件已移动
**解决方法：**
- 检查video目录是否存在于正确位置
- 使用 `-b` 参数指定正确的基础路径
- 确认文件名拼写正确

#### 3. "错误: 无法修改文件时间"
**原因：** 权限不足或文件被占用
**解决方法：**
- 以管理员身份运行脚本
- 确保视频文件未被其他程序占用
- 检查磁盘空间是否充足

#### 4. 编码错误
**原因：** HTML文件使用了不支持的字符编码
**解决方法：**
- 脚本自动尝试多种编码格式（UTF-8、GBK、Latin1）
- 如仍有问题，可手动转换HTML文件编码为UTF-8

### 调试技巧

1. **使用详细模式**：添加 `-v` 参数查看详细的处理信息
2. **测试单个文件**：先用单文件模式测试，确保脚本工作正常
3. **检查文件结构**：确保目录结构符合Memotrace的导出格式
4. **路径验证**：使用绝对路径避免相对路径问题

## 版本历史

### v2.1 (2025-06-09)
- ✅ 更新了正则表达式，以识别最新版 MemoTrace（v2.1.1）的 html 文件

### v2.0 (2025-06-09)
- ✅ 新增批量处理模式，支持处理多个聊天记录子文件夹
- ✅ 改进正则表达式，支持传统格式和JSON格式数据
- ✅ 重构命令行参数系统，使用互斥参数组
- ✅ 增强错误处理和统计信息显示
- ✅ 优化文件路径处理，支持子目录结构

### v1.0 (2025-06-09)
- ✅ 基本的HTML文件解析功能
- ✅ 视频文件时间戳修改功能
- ✅ 命令行参数支持
- ✅ 多种文本编码支持

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 联系方式

如有问题或建议，请创建GitHub Issue。
- **编码支持**：自动检测HTML文件编码（UTF-8、GBK、Latin1）
- **备份建议**：建议在运行前备份重要的视频文件
- **路径格式**：支持Windows风格路径（使用反斜杠）

## 技术实现

### 正则表达式模式

```python
pattern = r"text:\s*['\"](\./video/[^'\"]+\.mp4)['\"][^}]*?timestamp:\s*(\d+)"
```

此模式用于匹配：
- `text:` 后面跟着单引号或双引号包围的 `./video/xxx.mp4` 路径
- 同一数据块中的 `timestamp:` 后面跟着的数字

### 支持的数据格式

脚本能识别以下几种格式的数据：

```javascript
// 传统格式
{ type:43, text: './video/filename.mp4', timestamp:1514809949, ... }

// 传统格式（带空格）
{ type: 43, text: './video/filename.mp4', timestamp: 1514809949, ... }

// JSON格式（标准）
{"type": 43, "text": "./video/filename.mp4", "timestamp": 1514809949, ... }

// JSON格式（带子目录）
{"type": 43, "text": "./video/2024-01/filename.mp4", "timestamp": 1514809949, ... }

// 混合格式（部分属性有引号）
{ "type": 43, "text": "./video/filename.mp4", "timestamp": 1514809949 }
```

**路径支持：**
- ✅ 所有路径必须以 `./video/` 开头
- ✅ 支持单级和多级子目录
- ✅ 文件扩展名必须是 `.mp4`

## 依赖要求

- **Python版本**：Python 3.6 或更高版本
- **标准库模块**：
  - `os` - 文件系统操作
  - `re` - 正则表达式匹配
  - `datetime` - 时间戳转换
  - `argparse` - 命令行参数解析
  - `pathlib` - 路径处理

无需安装额外的第三方库，仅使用Python标准库。

## 故障排除

### 常见问题

1. **找不到匹配的视频文件和时间戳**
   - 检查HTML文件是否包含正确格式的数据
   - 确认数据格式符合 `text: './video/xxx.mp4'` 和 `timestamp: 数字` 的模式

2. **文件不存在警告**
   - 检查视频文件路径是否正确
   - 使用 `-b` 参数指定正确的视频文件基础目录
   - 确认HTML文件中的相对路径与实际文件结构匹配

3. **修改文件时间失败**
   - 检查是否有足够的文件系统权限
   - 确认文件未被其他程序占用
   - 在Windows系统中，可能需要管理员权限

4. **编码错误**
   - 脚本会自动尝试多种编码（UTF-8、GBK、Latin1）
   - 如仍有问题请检查HTML文件的实际编码格式

### 调试建议

- 使用 `-v` 参数获得详细的输出信息
- 使用小范围的测试文件先验证功能
- 检查控制台输出中的错误信息和警告
- 确认HTML文件和视频文件的目录结构

### 帮助信息

运行以下命令查看完整的帮助信息：

```bash
python update_video_mtime.py --help
```

## 许可证

本项目使用 MIT 许可证，详情请查看 LICENSE 文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系

如有问题或建议，请通过GitHub Issues联系。