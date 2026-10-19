#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验一批实验报告的批改产物。

检查：
  1. 每份提交的 PDF 都有对应的「_批改.pdf」副本；
  2. 批改副本首页含「批改意见」「最终得分」「徐海燕」，分数在 [70, 95]；
  3. 成绩单对应实验列里，每个已交学生都有分，且与 PDF 上的分数一致；
  4. 该列平均分在目标值 ±容差内。

任一检查失败以非零码退出。

用法：
  python scripts/verify_batch.py \
      --submitted "C:\\...\\计网实验报告1" \
      --graded    "C:\\...\\实验1批改" \
      --xlsx      "C:\\...\\计算机网络实验报告成绩单.xlsx" \
      --experiment 1 --target-mean 91
"""
import argparse
import glob
import os
import re
import sys

COL_BY_EXPERIMENT = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8}


def fail(errors, msg):
    errors.append(msg)


def main():
    ap = argparse.ArgumentParser(description="校验一批实验报告的批改产物")
    ap.add_argument("--submitted", required=True, help="提交的 PDF 目录")
    ap.add_argument("--graded", required=True, help="批改后的 PDF 目录")
    ap.add_argument("--xlsx", required=True, help="成绩单 xlsx")
    ap.add_argument("--experiment", type=int, default=1, choices=range(1, 7), help="第几个实验（1-6）")
    ap.add_argument("--target-mean", type=float, default=91.0, help="目标平均分")
    ap.add_argument("--tolerance", type=float, default=0.5, help="平均分允许偏差")
    args = ap.parse_args()

    try:
        import pymupdf
        import openpyxl
    except ImportError as e:
        print(f"[FAIL] 缺少依赖：{e}。先执行 pip install pymupdf pypdf openpyxl", file=sys.stderr)
        return 2

    errors = []
    warnings = []

    submitted = sorted(glob.glob(os.path.join(args.submitted, "*.pdf")))
    if not submitted:
        print(f"[FAIL] 提交目录里没有 PDF：{args.submitted}", file=sys.stderr)
        return 2

    scores = {}
    for path in submitted:
        name = os.path.basename(path)
        m = re.match(r"^(\d{12})[_-](.+?)[_-]实验(\d+)", name)
        if not m:
            warnings.append(f"文件名无法解析学号：{name}")
            continue
        sid = m.group(1)
        graded = os.path.join(args.graded, os.path.splitext(name)[0] + "_批改.pdf")
        if not os.path.exists(graded):
            fail(errors, f"缺少批改副本：{os.path.basename(graded)}")
            continue

        page_text = pymupdf.open(graded)[0].get_text()
        if "批改意见" not in page_text:
            fail(errors, f"缺批改意见：{os.path.basename(graded)}")
        if "徐海燕" not in page_text:
            fail(errors, f"缺教师签名：{os.path.basename(graded)}")
        sm = re.search(r"最终得分\s*[：:]\s*(\d+)", page_text)
        if not sm:
            fail(errors, f"缺最终得分：{os.path.basename(graded)}")
            continue
        score = int(sm.group(1))
        if not 70 <= score <= 95:
            fail(errors, f"分数越界 {score}：{os.path.basename(graded)}")
        scores[sid] = score

    col = COL_BY_EXPERIMENT[args.experiment]
    wb = openpyxl.load_workbook(args.xlsx, data_only=True)
    ws = wb.active
    sheet = {}
    for row in ws.iter_rows(min_row=3, values_only=True):
        sid = str(row[0]).strip() if row[0] is not None else ""
        if re.fullmatch(r"\d{12}", sid):
            sheet[sid] = row[col - 1]

    for sid, score in scores.items():
        if sid not in sheet:
            fail(errors, f"成绩单里没有学号 {sid}")
        elif sheet[sid] != score:
            fail(errors, f"学号 {sid} 分数不一致：成绩单={sheet[sid]} PDF={score}")

    vals = [v for v in sheet.values() if isinstance(v, (int, float))]
    if not vals:
        fail(errors, "成绩单该列没有任何分数")
        mean = None
    else:
        mean = sum(vals) / len(vals)
        if abs(mean - args.target_mean) > args.tolerance:
            fail(errors, f"平均分 {mean:.2f} 偏离目标 {args.target_mean}（容差 ±{args.tolerance}）")

    print(f"提交 {len(submitted)} 份，解析出 {len(scores)} 份，成绩单该列 {len(vals)} 个分数")
    if mean is not None:
        print(f"平均分：{mean:.2f}（目标 {args.target_mean} ±{args.tolerance}）")
    for w in warnings:
        print(f"[WARN] {w}")
    if errors:
        print(f"\n[FAIL] {len(errors)} 项问题：")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\n[OK] 全部检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
