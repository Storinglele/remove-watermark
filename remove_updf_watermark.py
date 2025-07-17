import fitz  # PyMuPDF
import shutil
import os

# 配置参数
SRC_PDF = "xxx.pdf"
PDF_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PDF_PATH = os.path.join(PDF_DIR, SRC_PDF)
BACKUP_PDF_PATH = os.path.join(PDF_DIR, SRC_PDF.replace('.pdf', '_backup.pdf'))
OUTPUT_PDF_PATH = os.path.join(PDF_DIR, SRC_PDF.replace('.pdf', '_no_watermark.pdf'))

# 1. 备份原文件
if not os.path.exists(BACKUP_PDF_PATH):
    shutil.copy(SRC_PDF_PATH, BACKUP_PDF_PATH)
    print(f"已备份原文件到: {BACKUP_PDF_PATH}")
else:
    print(f"备份文件已存在: {BACKUP_PDF_PATH}")

# 2. 打开PDF并处理第一页
with fitz.open(SRC_PDF_PATH) as doc:
    page = doc[0]  # 只处理第一页
    rect = page.rect
    # 左上角区域（宽度0%-20%，高度0%-20%）
    left_top = fitz.Rect(0, 0, rect.width * 0.2, rect.height * 0.09)

    # 无条件遮盖左上角区域
    page.add_redact_annot(left_top, fill=(1, 1, 1))
    page.apply_redactions()

    # 2.1 处理文本水印
    blocks = page.get_text("blocks")
    for b in blocks:
        x0, y0, x1, y1, text, *_ = b
        block_rect = fitz.Rect(x0, y0, x1, y1)
        if left_top.intersects(block_rect) and ("UPDF" in text or "WWW.UPDF.CN" in text):
            page.add_redact_annot(block_rect, fill=(1, 1, 1))
    page.apply_redactions()

    # 2.2 处理图片水印
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        try:
            img_rects = page.get_image_bbox(xref)
        except Exception:
            continue  # 跳过无法获取位置的图片
        if img_rects and left_top.intersects(img_rects):
            page.add_redact_annot(img_rects, fill=(1, 1, 1))
    page.apply_redactions()

    # 2.3 处理超链接水印
    links = page.get_links()
    for link in links:
        if link.get("uri") and "updf.cn" in link["uri"]:
            link_rect = fitz.Rect(link["from"])
            if left_top.intersects(link_rect):
                page.add_redact_annot(link_rect, fill=(1, 1, 1))
    page.apply_redactions()

    # 3. 保存新PDF
    doc.save(OUTPUT_PDF_PATH, incremental=False)
    print(f"已保存去水印后的PDF到: {OUTPUT_PDF_PATH}") 