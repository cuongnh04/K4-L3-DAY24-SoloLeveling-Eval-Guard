# Trạng thái bài nộp — 13/10/2026

Nguyễn Huy Cương — 2A202602842.

Đã triển khai Tasks 1–12, tích hợp m1–m5, chạy được 50 answers thật
và lưu `artifacts/answers_50q.json`. Có extractive fallback được đánh dấu
trong từng record. Bộ kiểm thử offline: 94 passed, 3 integration deselected.

**Chưa hoàn thành toàn bộ bài.** Chưa có ba artifact RAGAS/judge/guard hợp lệ,
ba báo cáo kỹ thuật vẫn là template; `check_lab.py` chưa thể pass.
Các batch live đã thử gặp giới hạn quota 429 và model quá tải 503.
RAGAS gặp lỗi endpoint không hỗ trợ nhiều candidates; adapter đã chuyển
answer_relevancy sang strictness=1 (một câu hỏi sinh ngược), cần chạy lại để xác minh.
Không tạo số đo hoặc nhãn giả để thay cho các batch thất bại.

Hướng dẫn chạy lại: [RUN.md](RUN.md). Dùng `API_INTERVAL_SECONDS` theo quota của model
(ví dụ 5 giây cho 15 RPM, 13 giây cho 5 RPM). Latency guard có bật limiter sẽ bao gồm
thời gian chờ limiter, phải nêu rõ trong báo cáo và không coi là latency thuần model.

Qdrant Docker tải lỗi mạng; lần sinh answers dùng Qdrant local in-memory.
Hai PDF scan chưa OCR. Các giới hạn này không được coi là đã hoàn tất chuẩn bị production.
