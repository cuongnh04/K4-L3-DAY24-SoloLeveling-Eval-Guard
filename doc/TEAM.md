# Day24 — Nguyễn Huy Cương

Tên nhóm: Nguyễn Huy Cương.
Repo: https://github.com/cuongnh04/K4-Track-3B-NguyenHuyCuong-Day24-Eval-Guard
Người nộp: Nguyễn Huy Cương — 2A202602842.
Ngày thực hiện: 12/10/2026, Asia/Ho_Chi_Minh. Deadline theo README lớp: 11:59 ngày 13/10/2026.
Commit dùng để chấm: commit hoàn thiện bài được ghi nhận trong lịch sử main.

| STT | Họ và tên | MSSV | Phạm vi | Bằng chứng |
|---|---|---|---|---|
| 1 | Nguyễn Huy Cương | 2A202602842 | Chủ repo, yêu cầu hoàn thiện và nộp; AI hỗ trợ code, kiểm thử và báo cáo | src/, tests/, artifacts/, doc/reports/ |

## Môi trường

Windows, Python 3.11 trong .runtime. Annoy 1.17.3 binary conda-forge; NeMo 0.10.0,
RAGAS 0.1.22, NumPy 1.26.4. Xem doc/RUN.md và requirements/constraints-core.txt.
Model IDs và thời điểm chạy chính xác nằm trong metadata của từng artifact.
Embedding multilingual MiniLM 384 chiều; NeMo embedding all-MiniLM-L6-v2.
Enrichment tùy chọn tắt, không sửa dữ liệu gốc. Qdrant server tải Docker lỗi EOF,
adapter sử dụng Qdrant local in-memory. Hai PDF scan không có text được loader
bỏ qua và cảnh báo; chưa OCR. Corpus Markdown giữ cả policy cũ và mới.

## INDIVIDUAL

### NguyenHuyCuong-2A202602842

- Phạm vi: tích hợp m1–m5, Phase A/B/C, kiểm thử và báo cáo bài Day24.
- AI hỗ trợ: Codex triển khai các hàm, xử lý tương thích môi trường, chạy batch,
  phân tích artifact và chuẩn bị commit/push theo yêu cầu chủ repo.
- Bằng chứng: source, tests và JSON thực nghiệm; không coi unit mock là lần chạy thật.
- Cách kiểm chứng: pytest, scripts/check_lab.py và đối chiếu metadata/source hashes.
- Kiến thức thể hiện trong bài: bốn metric RAGAS, nhóm yếu theo mean,
  swap-and-average, Cohen kappa, clean controls và latency có warm-up.
- Người học cần tự đọc và giải thích lại phần AI hỗ trợ; không khai việc tự viết code
  hoặc trải nghiệm cá nhân chưa được xác nhận.
- Nguồn pipeline: repo Day18 cùng tài khoản; m4 được viết adapter để dùng RAGAS thật
  và ghi provenance model. Mã scaffold và fixtures từ repo đề VinUni-AI20k.

## Cập nhật sau khi nộp

Chưa gửi link qua kênh coach trong phiên này. Push lên GitHub theo yêu cầu người dùng;
không đồng nghĩa đã nộp qua kênh lớp. Chưa có cập nhật sau deadline.