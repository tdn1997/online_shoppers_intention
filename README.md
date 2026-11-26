# Dự đoán khả năng mua hàng trên website

Đồ án phân loại phiên truy cập có dẫn đến mua hàng hay không. Random Forest đạt **Average Precision 0,3542** và phát hiện **223 trong 382 phiên mua** trên tập test đã chốt. Xem [bản Report](submission/Report.html) và [slide bảo vệ tiếng Anh](submission/Presentation.pptx).

## Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| [`data/`](data/) | CSV gốc, chỉ mục train/test và mô tả biến. |
| [`notebooks/`](notebooks/) | Sáu notebook thực nghiệm theo thứ tự chạy. |
| [`submission/`](submission/) | Proposal, Milestone và Report kèm HTML, cùng PowerPoint tiếng Anh. |
| [`reports/`](reports/) | Bảng điểm validation dùng để tái lập Milestone và bước đánh giá. |
| [`docs/`](docs/) | Kế hoạch, phân công bảo vệ, Q&A và mẫu Peer Assessment. |

`demo.py` là lệnh mở demo. `project_model.py` chứa cách đọc split và cấu hình Random Forest dùng chung.

## 1. Cài đặt

Chạy các lệnh từ thư mục gốc của bản clone. Đồ án chạy trên CPU. Bộ phiên bản trong `requirements.txt` đã được kiểm chứng trên Windows với Python **3.15.2**. Các lệnh macOS dùng cùng phiên bản Python và thư viện, nhưng quy trình chưa được chạy thử trực tiếp trên máy Mac.

Nếu bạn chỉ cần xem hồ sơ đã xuất, mở [Report.html](submission/Report.html), [Milestone.html](submission/Milestone.html) hoặc [Proposal.html](submission/Proposal.html) bằng trình duyệt.

### Windows

Mở PowerShell. Kiểm tra kết quả lệnh đầu tiên là Python **3.15.2** trước khi tạo môi trường.

```powershell
py -3.15 --version
py -3.15 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip check
```

Nếu máy thiếu lệnh `py` nhưng `python --version` trả về Python 3.15.2, dùng `python -m venv .venv` cho bước tạo môi trường. Khi chạy trong VS Code, cài các extension **Python** và **Jupyter**, mở notebook rồi chọn kernel `.venv/Scripts/python.exe`.

### macOS

Mở Terminal sau khi cài Python **3.15.2**. Tạo `.venv` ngay trên máy Mac.

```bash
python3.15 --version
python3.15 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Khi chạy trong VS Code, cài các extension **Python** và **Jupyter**, mở notebook rồi dùng **Select Kernel** để chọn `.venv/bin/python`.

## 2. Chạy lại thí nghiệm

CSV và `split_indices.json` đã có trong [data/](data/). Giữ nguyên CSV và thứ tự dòng để mã SHA-256 khớp với split đã lưu. Dataset **Online Shoppers Purchasing Intention** có 12.330 phiên, 17 feature gốc và nhãn `Revenue`. Pipeline chính bỏ `PageValues` và dùng 16 feature. [Sakar và Kastro, UCI Machine Learning Repository, 2018, CC BY 4.0](https://doi.org/10.24432/C5F88Q)

| Thứ tự | Notebook | Nội dung |
|---:|---|---|
| 1 | [EDA](notebooks/01_eda.ipynb) | Kiểm tra dữ liệu, đọc split 80/20 và vẽ biểu đồ trên train. |
| 2 | [Huấn luyện](notebooks/02_training.ipynb) | So sánh năm mô hình trên 5 fold train và ghi `reports/validation_scores.csv`. |
| 3 | [Đánh giá](notebooks/03_evaluation.ipynb) | Chọn ngưỡng từ dự đoán out-of-fold trên train và tái lập kết quả test của cấu hình tuần 3. |
| 4 | [Kiểm tra độ ổn định](notebooks/04_robustness.ipynb) | Grouped CV, đường Precision–Recall và nested CV với 12 cấu hình Random Forest. |
| 5 | [Learning curve](notebooks/05_learning_curve.ipynb) | AP trên các fold nhóm khi tăng số phiên fit. |
| 6 | [Kiểm tra feature và độ tin cậy](notebooks/06_model_review.ipynb) | So sánh `PageValues`, biến ngữ cảnh và boosting, kiểm tra calibration và tính khoảng bootstrap trên test. |

Chọn **Run All** theo thứ tự trên hoặc chạy lệnh tương ứng từ thư mục gốc. Notebook 04 có thể mất vài phút. Tùy chọn `--inplace` lưu lại output vào notebook và notebook 02 ghi lại bảng `reports/validation_scores.csv`.

**Windows**

```powershell
.venv/Scripts/jupyter-execute.exe notebooks/01_eda.ipynb notebooks/02_training.ipynb notebooks/03_evaluation.ipynb notebooks/04_robustness.ipynb notebooks/05_learning_curve.ipynb notebooks/06_model_review.ipynb --inplace --timeout=600
```

**macOS**

```bash
.venv/bin/jupyter-execute notebooks/01_eda.ipynb notebooks/02_training.ipynb notebooks/03_evaluation.ipynb notebooks/04_robustness.ipynb notebooks/05_learning_curve.ipynb notebooks/06_model_review.ipynb --inplace --timeout=600
```

## 3. Hồ sơ nộp và bảo vệ

| Hạng mục | File |
|---|---|
| Proposal | [Notebook](submission/Proposal.ipynb) · [HTML](submission/Proposal.html) |
| Milestone | [Notebook](submission/Milestone.ipynb) · [HTML](submission/Milestone.html) |
| Report | [Notebook](submission/Report.ipynb) · [HTML](submission/Report.html) |
| Presentation | [PowerPoint tiếng Anh](submission/Presentation.pptx) |
| Kế hoạch | [Tiến độ và checklist trước khi nộp](docs/PLAN.md) |
| Video và Q&A | [Kế hoạch diễn tập và câu hỏi](docs/defense.md) |
| Peer Assessment | [Mẫu phiếu cá nhân](docs/peer_assessment.md) |

Mở các bản HTML bằng trình duyệt để đọc hoặc nộp bài. Milestone và Report đã lưu bảng kết quả trong bản HTML, riêng Report còn có hình minh họa. Khi cần xuất lại, chạy hai lệnh dưới đây từ thư mục gốc. Lệnh đầu cập nhật output của Milestone và Report, dùng bảng validation đã lưu hoặc bảng mới tạo ở bước 2. Lệnh sau xuất cả ba notebook thành HTML trong `submission/`. Xem phần phụ lục của Report để tra các thử nghiệm về grouped CV, ngưỡng, learning curve, feature và calibration.

**Windows**

```powershell
.venv/Scripts/jupyter-execute.exe submission/Milestone.ipynb submission/Report.ipynb --inplace --timeout=600
.venv/Scripts/jupyter-nbconvert.exe --to html --embed-images --no-input --output-dir submission submission/Proposal.ipynb submission/Milestone.ipynb submission/Report.ipynb
```

**macOS**

```bash
.venv/bin/jupyter-execute submission/Milestone.ipynb submission/Report.ipynb --inplace --timeout=600
.venv/bin/jupyter-nbconvert --to html --embed-images --no-input --output-dir submission submission/Proposal.ipynb submission/Milestone.ipynb submission/Report.ipynb
```

## Chạy demo Gradio cục bộ (tùy chọn)

Bạn có thể chạy demo ngay sau bước cài đặt.

**Windows**

```powershell
.venv/Scripts/python.exe demo.py
```

**macOS**

```bash
.venv/bin/python demo.py
```

Mở `http://127.0.0.1:7860`, chọn một phiên mẫu rồi nhấn **Submit**. Có thể sửa các giá trị đầu vào và chạy lại. Demo fit Random Forest cấu hình tuần 3 trên train lúc khởi động, sau đó trả điểm mua gốc từ 0 đến 1 và nhãn theo ngưỡng **0,20965**. Điểm dùng để xếp hạng và gán nhãn trong minh họa offline với dữ liệu tổng hợp theo phiên. Xem [kiểm tra calibration](notebooks/06_model_review.ipynb) để biết mức độ khớp với tỷ lệ mua quan sát. Nhấn **Ctrl+C** để dừng. Nếu cổng bận, truyền `--port 7861` và mở cổng tương ứng.
