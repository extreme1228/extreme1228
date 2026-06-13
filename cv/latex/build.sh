#!/usr/bin/env bash
# Build both CV PDFs (Chinese + English) with xelatex.
# Requires: TeX Live with xelatex, ctex/xeCJK, fontawesome5; macOS system fonts
# (Songti SC / Heiti SC) for Chinese. Run from this directory.
set -euo pipefail
cd "$(dirname "$0")"

for f in resume_zh resume_en; do
  echo "==> Building $f ..."
  xelatex -interaction=nonstopmode -halt-on-error "$f.tex" >/dev/null
done

cp resume_zh.pdf "../吕博文-简历-2026.pdf"
cp resume_en.pdf "../Bowen-Lv-CV-2026.pdf"

# tidy build artifacts
rm -f ./*.aux ./*.log ./*.out
echo "Done. PDFs copied to ../ (吕博文-简历-2026.pdf, Bowen-Lv-CV-2026.pdf)"
