# Chạy bài Day24

Nguyễn Huy Cương — 2A202602842.

## Môi trường Windows

Annoy cần compiler khi cài từ PyPI. Bản chạy này dùng binary chính thức từ
conda-forge rồi cài các dependency đã pin của starter:

```powershell
conda create --prefix .runtime -c conda-forge python=3.11 python-annoy=1.17.3 pip -y
uv pip install --python .runtime/python.exe -r requirements/requirements.txt -c requirements/constraints-core.txt
uv pip install --python .runtime/python.exe https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

Sao chép `.env.example` thành `.env`, cấu hình key/model và endpoint.
Gemini sử dụng [OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai).
Không đưa key thật vào Git. Các tên model chỉ dùng được nếu tài khoản có quyền truy cập.

```powershell
docker compose -f infra/docker-compose.yml up -d
.runtime/python.exe scripts/setup_answers.py --live
.runtime/python.exe scripts/run_experiments.py --phase a --live
.runtime/python.exe scripts/run_experiments.py --phase b --live
.runtime/python.exe scripts/run_experiments.py --phase c --live --latency-samples 20
.runtime/python.exe scripts/check_lab.py --with-tests
```

Các lệnh `--live` gọi API có tính phí. Không chạy lại nếu chỉ muốn kiểm tra kết quả:
dùng `scripts/check_lab.py`. Qdrant ưu tiên server; adapter Day18 có fallback
in-memory khi server không truy cập được. Embedding, model và dimension phải khớp.
Presidio dùng spaCy `en_core_web_sm` và các recognizer CCCD/CMND, điện thoại VN,
email. `ENRICHMENT_ENABLED=0` giữ nguyên nội dung corpus và bỏ enrichment tùy chọn.

Nguồn m1/m2/m3/m5: repo Day18 của cùng tài khoản, được điều chỉnh theo giao diện Day24.
M4 dùng RAGAS thật; không thay metric lỗi bằng số giả. Các file fixtures và ground truth
được giữ nguyên, không dùng reference để sinh answer. Metadata ghi model theo từng vai trò.
