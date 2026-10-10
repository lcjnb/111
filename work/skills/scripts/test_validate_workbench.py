"""校验脚本测试：覆盖标记缺失、废标与评分混表、符号计数不符。"""

import tempfile
import unittest
from pathlib import Path

from validate_workbench import TAGS, validate


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ValidateWorkbenchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "N5100012026002044"
        self.project.mkdir(parents=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_reports_missing_content_tag(self) -> None:
        write(self.project / "30_投标文件提纲.md", "## 技术方案\n本项目将建设课程平台。\n")
        report = validate(self.project)
        self.assertTrue(any("缺少内容标记" in e for e in report["errors"]))

    def test_reports_mixed_rejection_and_score_tables(self) -> None:
        write(
            self.project / "02_废标项清单.md",
            "# 废标项清单\n\n## 评分项\n\n| 条款 | 分值 |\n| --- | --- |\n| 实施方案 | 9分 |\n",
        )
        report = validate(self.project)
        self.assertTrue(any("混表" in e for e in report["errors"]))

    def test_reports_symbol_count_mismatch(self) -> None:
        write(self.project / "01_要求矩阵.md", "# 要求矩阵\n\n无符号条目。\n")
        write(
            self.project / "03_评分点清单.md",
            "# 评分点清单\n\n符号计数：▲=11（本项目应为 12）\n",
        )
        report = validate(self.project)
        self.assertTrue(any("符号计数" in e for e in report["errors"]))

    def test_passes_when_tags_and_counts_are_consistent(self) -> None:
        tag = TAGS[0]
        write(self.project / "01_要求矩阵.md", f"# 要求矩阵\n\n- {tag} 课程平台须提供截图。\n")
        write(
            self.project / "02_废标项清单.md",
            "# 废标项清单\n\n- " + TAGS[0] + " 响应有效期不少于 90 天。\n",
        )
        write(
            self.project / "03_评分点清单.md",
            "# 评分点清单\n\n符号计数：▲=12、●=10、█=3（与评审细则一致）\n",
        )
        report = validate(self.project)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
