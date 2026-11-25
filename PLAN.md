# Kế hoạch đồ án Dự đoán khả năng mua hàng trên website

Phân loại offline khả năng mua hàng từ dữ liệu tổng hợp của một phiên truy cập. Lớp dương là `Revenue=True`. Triển khai cá nhân trong Windows, VS Code và Jupyter Notebook, sử dụng Python trong `.venv` và các thư viện miễn phí chạy bằng CPU.

Ba tuần dưới đây là mốc dự kiến. Chưa tìm thấy Proposal hoặc tài liệu hướng dẫn của giảng viên trong workspace, nên hạn nộp, mẫu Milestone và định dạng nộp báo cáo vẫn chưa xác minh.

## Trạng thái workspace

- [x] Đã kiểm tra workspace và các thư mục cha để tìm `AGENTS.md`. Không tìm thấy file này.
- [x] Đã xác minh `.venv` có Python 3.15.2 và các thư viện cần thiết. Notebook đã chạy bằng kernel từ `.venv`.
- [x] Đã đọc `data/online_shoppers_intention.csv`. CSV có 12.330 phiên, 17 feature và nhãn `Revenue`. Có 1.908 phiên mua (15,47%). [Nguồn dữ liệu UCI](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
- [x] Đã chạy và lưu output trong `01_eda.ipynb`. Notebook có kết quả kiểm tra dữ liệu, thống kê split, ba biểu đồ và bốn nhận xét trên train. Output ghi nhận 0 giá trị thiếu và 125 dòng trùng hoàn toàn được giữ lại.
- [x] Đã lưu index của split vào `data/split_indices.json` và xác minh lần chạy sau đọc lại đúng các vị trí dòng.
- [x] Đã chạy `02_training.ipynb`, xuất bảng validation và viết Milestone. Random Forest có Average Precision trung bình cao nhất trên validation (0,3762).
- [x] Đã chạy `03_evaluation.ipynb` và hoàn thành Report cùng 8 slide PowerPoint. Random Forest đạt AP 0,3542 trên test.

## Cấu trúc thư mục đề xuất

```text
.
├── .venv/                         # Có sẵn
├── README.md
├── requirements.txt
├── PLAN.md
├── 01_eda.ipynb                   # Có sẵn
├── 02_training.ipynb              # Có sẵn
├── 03_evaluation.ipynb            # Có sẵn
├── 04_robustness.ipynb            # Phân tích bổ sung trên train
├── 05_learning_curve.ipynb        # Learning curve theo nhóm
├── demo.py                        # Gradio cục bộ
├── project_model.py               # Split train và cấu hình Random Forest
├── data/
│   ├── online_shoppers_intention.csv  # Có sẵn
│   └── split_indices.json             # Có sẵn
└── reports/
    ├── validation_scores.csv      # Có sẵn
    ├── milestone.md               # Có sẵn
    ├── report.md                  # Có sẵn
    └── slides.pptx                # Có sẵn
```

Giữ CSV gốc theo đúng thứ tự dòng và dùng đường dẫn tương đối từ thư mục gốc. Sau khi đọc CSV, đặt `y = df["Revenue"]` và tạo `X` bằng cách bỏ `Revenue` cùng `PageValues` trong cấu hình chính. Các chỉ số dòng lưu trong `split_indices.json` là vị trí dòng dữ liệu bắt đầu từ 0, theo thứ tự khi đọc CSV gốc. Hai notebook sau dùng danh sách vị trí đã lưu để lấy dòng bằng `.iloc`, giữ nguyên thứ tự trong mỗi tập và kiểm tra SHA-256 của CSV trước khi dùng. Nếu CSV thay đổi, dừng và kiểm tra nguồn dữ liệu vì các vị trí đã lưu có thể trỏ sang phiên khác.

## Tuần 1 · Dữ liệu và EDA

- [x] **1. Chuẩn bị đầu vào.** Xác minh `.venv`, các thư viện cần thiết và vị trí CSV trong workspace.
- [x] **2. Kiểm tra schema và chất lượng dữ liệu.** Xem kiểu dữ liệu, dữ liệu thiếu, dòng trùng và phân bố `Revenue`. Giữ dòng trùng vì CSV thiếu mã phiên để phân biệt các phiên có cùng giá trị tổng hợp. Ghi chú rằng `OperatingSystems`, `Browser`, `Region` và `TrafficType` là mã phân loại.
- [x] **3. Xác lập split.** Notebook đã chia bằng `train_test_split(test_size=0.2, random_state=42, stratify=y)`. Output lưu 9.864 phiên train (15,47% mua), 2.466 phiên test (15,49% mua) và 0 index chung.
- [x] **4. Kiểm tra EDA trên train.** Output có phân bố nhãn, phân bố `ProductRelated` và `ProductRelated_Duration` theo nhãn, cùng bốn nhận xét định lượng.
- [x] **5. Lưu split hiện tại.** `01_eda.ipynb` đã ghi danh sách index theo thứ tự của từng tập, cấu hình chia, số dòng và SHA-256 của CSV vào `data/split_indices.json`. Các lần chạy sau đọc lại split đã lưu để chạy EDA.
- [x] **6. Kiểm tra đầu ra sau khi lưu split.** Đã chạy notebook hai lần từ thư mục gốc để kiểm tra cả tạo và đọc split. Hai tập rời nhau, từng tập có index duy nhất, phủ đủ 12.330 dòng, và có lần lượt 1.526 và 382 phiên mua. Phần dẫn nhập ghi rõ đánh giá test diễn ra ở tuần 3. Output của lần đọc split đã được lưu.

**Đầu ra** gồm `01_eda.ipynb` và `data/split_indices.json`.

**Tuần 1 hoàn thành khi** notebook chạy từ thư mục gốc với kernel `.venv`, lưu ba biểu đồ và nhận xét từ train, đồng thời khôi phục được split có đúng số dòng và tỷ lệ lớp đã kiểm tra.

## Tuần 2 · Huấn luyện và Milestone

- [x] **1. Đọc split đã lưu.** `02_training.ipynb` xác minh CSV và index, rồi dùng 9.864 phiên train với bộ 16 feature chính.
- [x] **2. Dựng preprocessing.** `ColumnTransformer` trong `Pipeline` one-hot encode biến phân loại với `handle_unknown="ignore"`. Các biến số được scale cho Logistic Regression và kNN. Decision Tree và Random Forest dùng thang số gốc. Toàn bộ pipeline được fit bên trong từng fold.
- [x] **3. Chạy baseline và mô hình đầu tiên.** Đã chạy `DummyClassifier` rồi Logistic Regression. Mọi mô hình dùng cùng bộ fold từ `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` trên train.
- [x] **4. So sánh thêm ba mô hình.** Đã chạy kNN, Decision Tree và Random Forest trên CPU. Bảng CSV lưu Average Precision từng fold, trung bình, độ lệch chuẩn, tham số và thời gian.
- [x] **5. Viết Milestone.** Đã ghi tiến độ, kết quả validation của năm mô hình, khó khăn và các việc tiếp theo cho tuần 3.

**Đầu ra** gồm `02_training.ipynb`, `reports/validation_scores.csv` và `reports/milestone.md`.

**Tuần 2 hoàn thành khi** cả năm mô hình có điểm validation đo trên cùng bộ fold và bảng điểm cùng Milestone đủ thông tin để chọn cấu hình ở tuần 3.

## Tuần 3 · Đánh giá và báo cáo

Theo góp ý của giảng viên, bỏ Accuracy khỏi bộ chỉ số báo cáo. Trên tập train, nếu dự đoán mọi phiên là không mua, Accuracy vẫn đạt 84,53% trong khi Recall của lớp mua bằng 0. Giữ Average Precision làm chỉ số chính.

- [x] **1. Chốt cấu hình trước khi đánh giá test.** Chọn Random Forest theo AP trung bình trên validation. Giữ bộ 16 feature và cấu hình tuần 2. Chốt ngưỡng 0,20964924233624288 bằng cách tối đa hóa F1 lớp mua trên dự đoán out-of-fold của train.
- [x] **2. Đánh giá cuối.** Đã chạy `03_evaluation.ipynb` bằng `.venv`, fit pipeline trên toàn bộ train và đánh giá trên 2.466 phiên test đã lưu. Notebook có AP, ROC-AUC, Precision, Recall, F1 của lớp mua và confusion matrix.
- [x] **3. Phân tích lỗi.** Đã thống kê 159 false negative và 513 false positive, so sánh feature giữa các nhóm và xem ví dụ theo điểm dự đoán.
- [x] **4. Hoàn thiện Report và slide.** Đã viết báo cáo, tạo 8 slide PowerPoint và đối chiếu số liệu test với output notebook.

**Đầu ra** gồm `03_evaluation.ipynb` với bảng kết quả test và confusion matrix, `reports/report.md` và `reports/slides.pptx`.

**Tuần 3 hoàn thành khi** notebook chạy từ đầu đến cuối, lưu đủ chỉ số test và phân tích lỗi. Report và slide thống nhất số liệu với notebook và ghi rõ cấu hình đã chốt trước khi mở test.

## Mở rộng nếu còn thời gian

- [x] Kiểm tra vững bằng `StratifiedGroupKFold` trên train cho Random Forest và Logistic Regression. Cả năm fold theo nhóm có 0 dòng validation trùng vector feature với phần fit.
- [x] Vẽ Precision–Recall từ dự đoán out-of-fold theo nhóm và so sánh ngưỡng tuần 3 với ngưỡng ưu tiên Precision.
- [x] Thử 12 cấu hình Random Forest bằng nested grouped CV trên train. Kết quả fold ngoài chưa cải thiện AP, nên giữ cấu hình tuần 3 cho báo cáo test.
- [x] Vẽ learning curve theo nhóm ở các mốc 25%, 50%, 75% và 100% số nhóm fit.
- [x] Bổ sung slide về độ ổn định của kết quả từ grouped CV và nested CV.
- [x] Viết README, khóa phiên bản thư viện trong `requirements.txt` và tái lập kết quả của cả năm notebook trong bản clone với `.venv` mới.
- [ ] So sánh có và không có `PageValues` trên cùng fold train/validation, ghi rõ rủi ro leakage liên quan đến tín hiệu giao dịch.
- [x] Làm demo Gradio cục bộ từ pipeline đã chốt. Hai phiên mẫu minh họa cả hai nhãn, điểm mua qua API khớp với dự đoán trực tiếp của pipeline.

## Checklist buổi làm đầu tiên

- [x] Chạy `01_eda.ipynb` từ thư mục gốc bằng kernel `.venv/Scripts/python.exe`.
- [x] Cập nhật ô chia tập trong `01_eda.ipynb` để ghi `data/split_indices.json` từ cấu hình `test_size=0.2, random_state=42, stratify=y`. File chứa danh sách vị trí theo thứ tự, cấu hình chia, số dòng và SHA-256 của CSV.
- [x] Đọc split đã lưu và xác minh 9.864/2.466 phiên, 1.526/382 phiên mua, index duy nhất trong từng tập, hai tập rời nhau và toàn bộ 12.330 dòng được phủ.
- [x] Đổi ghi chú về thời điểm đánh giá cuối trong notebook sang tuần 3. Chạy lại toàn bộ, lưu output và xác minh ba biểu đồ cùng bốn nhận xét từ train.
