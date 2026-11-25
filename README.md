# Dự đoán khả năng mua hàng trên website

Đồ án phân loại phiên truy cập có dẫn đến mua hàng hay không. Random Forest đạt **Average Precision 0,3542** và phát hiện **223 trong 382 phiên mua** trên tập test đã chốt. Xem [báo cáo](reports/report.md) và [slide bảo vệ](reports/slides.pptx).

## Cài đặt

Chạy các lệnh từ thư mục gốc của bản clone. Đồ án chạy trên CPU. Bộ phiên bản trong `requirements.txt` đã được kiểm chứng trên Windows với Python **3.15.2**. Các lệnh macOS bên dưới dùng cùng phiên bản Python và thư viện.

### Windows

Mở PowerShell.

```powershell
python --version
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip check
```

Nếu có nhiều bản Python, dùng `py -3.15 -m venv .venv` để chọn Python 3.15. Trong VS Code, mở notebook và chọn kernel `.venv/Scripts/python.exe`.

### macOS

Mở Terminal sau khi cài Python **3.15.2**. Tạo `.venv` ngay trên máy Mac.

```bash
python3.15 --version
python3.15 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Trong VS Code, mở notebook rồi dùng **Select Kernel** để chọn `.venv/bin/python`.

## Chạy lại thí nghiệm

| Thứ tự | Notebook | Nội dung |
|---:|---|---|
| 1 | [EDA](01_eda.ipynb) | Kiểm tra dữ liệu, đọc split 80/20 và vẽ biểu đồ trên train. |
| 2 | [Huấn luyện](02_training.ipynb) | So sánh năm mô hình trên 5 fold train và ghi `reports/validation_scores.csv`. |
| 3 | [Đánh giá](03_evaluation.ipynb) | Chọn ngưỡng từ dự đoán out-of-fold trên train và tái lập kết quả test của cấu hình tuần 3. |
| 4 | [Kiểm tra độ ổn định](04_robustness.ipynb) | Grouped CV, đường Precision–Recall và nested CV với 12 cấu hình Random Forest. |
| 5 | [Learning curve](05_learning_curve.ipynb) | AP trên các fold nhóm khi tăng số phiên fit. |

Chọn **Run All** trên từng notebook hoặc chạy lệnh tương ứng từ thư mục gốc. Notebook 04 có thể mất vài phút.

**Windows**

```powershell
.venv/Scripts/jupyter-execute.exe 01_eda.ipynb 02_training.ipynb 03_evaluation.ipynb 04_robustness.ipynb 05_learning_curve.ipynb --inplace --timeout=600
```

**macOS**

```bash
.venv/bin/jupyter-execute 01_eda.ipynb 02_training.ipynb 03_evaluation.ipynb 04_robustness.ipynb 05_learning_curve.ipynb --inplace --timeout=600
```

CSV và `split_indices.json` đã có trong [data/](data/). Giữ nguyên CSV và thứ tự dòng để mã SHA-256 khớp với split đã lưu. Dataset **Online Shoppers Purchasing Intention** có 12.330 phiên, 17 feature gốc và nhãn `Revenue`. Pipeline chính bỏ `PageValues` và dùng 16 feature. [Sakar và Kastro, UCI Machine Learning Repository, 2018, CC BY 4.0](https://doi.org/10.24432/C5F88Q)

## Chạy demo Gradio cục bộ

**Windows**

```powershell
.venv/Scripts/python.exe demo.py
```

**macOS**

```bash
.venv/bin/python demo.py
```

Mở `http://127.0.0.1:7860`, chọn một phiên mẫu rồi nhấn **Submit**. Có thể sửa các giá trị đầu vào và chạy lại. Demo fit Random Forest cấu hình tuần 3 trên train lúc khởi động, sau đó trả điểm mua và nhãn theo ngưỡng **0,20965**. Điểm mua dùng để minh họa trên dữ liệu tổng hợp của phiên. Nhấn **Ctrl+C** để dừng. Nếu cổng bận, truyền `--port 7861` và mở cổng tương ứng.

## Đọc kết quả

- [Milestone](reports/milestone.md) tóm tắt so sánh mô hình trên validation.
- [Báo cáo](reports/report.md) có kết quả test, phân tích lỗi và phụ lục các thử nghiệm trên train.
- [Slide PowerPoint](reports/slides.pptx) trình bày bài toán, phương pháp, kết quả và độ ổn định.
