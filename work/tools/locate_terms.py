"""Locate key tender clauses in the source PDF and emit page numbers as JSON."""

import json
import sys
from pathlib import Path

from pypdf import PdfReader

PDF = Path(
    "AI赋能铁道移动通信课程建设及智能体开发与应用课程资源建设(二次)"
    "磋商文件（N510001202600204420260828001）.pdf"
)

TERMS = [
    "专门面向中小企业",
    "预算及最高限价",
    "650,000.00",
    "不接受联合体",
    "响应有效期",
    "90 天",
    "履约保证金",
    "5.0%",
    "服务期限",
    "300 日",
    "服务地点",
    "付款进度安排",
    "40.00%",
    "60.00%",
    "技术及服务指标",
    "履约能力",
    "类似业绩",
    "项目实施方案",
    "报价得分",
    "以 PDF 格式内容为准",
    "解密时间为 30 分钟",
    "符合性审查",
    "资格审查",
    "异常低价",
    "电子印章",
    "蜀ICP备",
]


def main() -> None:
    reader = PdfReader(str(PDF))
    page_text = [(page.extract_text() or "") for page in reader.pages]
    result = {}
    squeezed = ["".join(text.split()) for text in page_text]
    for term in TERMS:
        compact = "".join(term.split())
        pages = []
        for number, text in enumerate(squeezed, start=1):
            if compact in text:
                pages.append(number)
        result[term] = pages
    result["_total_pages"] = len(reader.pages)
    Path("tools/term_pages.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("written tools/term_pages.json")


if __name__ == "__main__":
    sys.exit(main())
