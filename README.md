# remove-watermark

本项目用于去除 PDF 文件（如 UPDF 导出的带水印文件）第一页左上角的水印内容，包括文本水印、图片水印和超链接水印。

## 使用方法

1. 安装依赖：

    ```bash
    python3 -m pip install PyMuPDF
    ```

2. 将需要去水印的 PDF 文件重命名为 `xxx.pdf`，并放置在项目目录下。

3. 运行脚本：

    ```bash
    python remove_updf_watermark.py
    ```

4. 处理结果：
    - 原 PDF 文件会备份为 `xxx_backup.pdf`
    - 去水印后的 PDF 文件输出为 `xxx_no_watermark.pdf`

## 依赖

- PyMuPDF

## 文件说明

- `remove_updf_watermark.py`：主脚本，负责去除水印。
- `requirements.txt`：依赖列表。
- `README.md`：项目说明文件。

## 注意事项

- 当前脚本仅处理第一页左上角区域的水印（宽度 0%-20%，高度 0%-9%）。
- 如有更多需求请根据实际情况调整代码逻辑，也可提交issue共同完善。