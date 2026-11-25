# Milestone tuần 2 · Dự đoán khả năng mua hàng trên website

## Tiến độ

- Tuần 1 đã kiểm tra dữ liệu, thực hiện EDA trên train và lưu split phân tầng 80/20 với `random_state=42`.
- Tuần 2 đã chạy năm mô hình trên 9.864 phiên train, trong đó 1.526 phiên mua (15,47%). Đã xác minh SHA-256 của CSV và dùng đúng vị trí dòng trong split đã lưu.
- Cấu hình chính dùng 16 feature. `Revenue` là nhãn và `PageValues` được loại để giảm nguy cơ leakage từ tín hiệu liên quan đến giao dịch. One-hot encoding nằm trong `Pipeline`. Logistic Regression và kNN có thêm scaling cho biến số. Preprocessing được fit lại trong phần training của từng fold.
- Mọi mô hình dùng chung 5 fold từ `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`. Tập test gồm 2.466 phiên được giữ cho tuần 3.

## Kết quả sơ bộ

Average Precision (AP) đo chất lượng xếp hạng phiên có mua. Thời gian fit dưới đây là số giây trung bình mỗi fold trên máy chạy notebook.

| Mô hình | Cấu hình chạy | AP trung bình | Độ lệch chuẩn AP | Fit (giây/fold) |
|---|---|---:|---:|---:|
| Random Forest | 100 cây, `max_depth=12`, `min_samples_leaf=5`, `random_state=42` | 0,3762 | 0,0294 | 0,3883 |
| Logistic Regression | `max_iter=1000` | 0,3232 | 0,0196 | 0,0556 |
| Decision Tree | `max_depth=5`, `min_samples_leaf=20`, `random_state=42` | 0,3180 | 0,0155 | 0,0336 |
| kNN | `n_neighbors=25` | 0,2839 | 0,0217 | 0,0138 |
| DummyClassifier | `strategy="prior"` | 0,1547 | 0,0002 | 0,0098 |

Random Forest có AP trung bình cao nhất, hơn Logistic Regression 0,0530 và baseline 0,2215. AP của Random Forest dao động từ 0,3463 đến 0,4293 giữa các fold. Các số này dùng để so sánh cấu hình trên validation.

Mã và output nằm trong [notebook huấn luyện](../02_training.ipynb). Điểm từng fold, tham số đầy đủ và thời gian nằm trong [bảng validation](validation_scores.csv).

## Khó khăn và giới hạn

- Nhãn mua chiếm 15,47% trên train. AP là chỉ số chính để so sánh việc xếp hạng lớp mua.
- CSV thiếu mã phiên để xác định các dòng có giá trị tổng hợp giống nhau có đến từ cùng một phiên hay không. Các dòng này được giữ theo quyết định ở tuần 1, nên giá trị giống nhau có thể xuất hiện ở cả phần fit và validation.
- Kết quả phản ánh các cấu hình ban đầu và có dao động qua fold. Các lựa chọn `class_weight` và ngưỡng phân loại sẽ cần được kiểm tra trên train/validation nếu thử tiếp.

## Việc tiếp theo

1. Chốt mô hình, preprocessing, tham số và ngưỡng từ train/validation. Random Forest là ứng viên dẫn đầu theo AP hiện tại.
2. Fit pipeline đã chốt trên toàn bộ train và đánh giá một lần trên tập test đã lưu. Báo cáo AP, ROC-AUC, Precision, Recall, F1 của lớp mua và confusion matrix. Theo góp ý của giảng viên, bỏ Accuracy khỏi báo cáo vì tỷ lệ lớp không mua cao có thể che khuất việc bỏ sót phiên mua.
3. Phân tích false negative và false positive, sau đó hoàn thiện Report và slide từ kết quả đã xác minh.
