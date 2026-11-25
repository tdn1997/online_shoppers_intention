# Dự đoán khả năng mua hàng trên website

## Tóm tắt

Random Forest đạt Average Precision (AP) **0,3542** và ROC-AUC **0,7610** trên 2.466 phiên test. Với ngưỡng chọn trên train, mô hình phát hiện **223 trong 382 phiên mua** và báo nhầm **513 phiên không mua**. Kết quả đánh giá khả năng phân loại offline từ dữ liệu tổng hợp theo phiên.

## 1. Dữ liệu và khám phá

Dataset **Online Shoppers Purchasing Intention** gồm 12.330 phiên, 17 feature gốc và nhãn `Revenue`. Có 1.908 phiên mua (15,47%). Dữ liệu có 0 giá trị thiếu. Giữ 125 dòng trùng hoàn toàn vì CSV thiếu mã phiên để phân biệt các phiên có cùng giá trị tổng hợp. [Sakar và Kastro, UCI Machine Learning Repository, 2018](https://doi.org/10.24432/C5F88Q)

| Tập | Số phiên | Phiên mua | Tỷ lệ mua |
|---|---:|---:|---:|
| Train | 9.864 | 1.526 | 15,47% |
| Test | 2.466 | 382 | 15,49% |

Split phân tầng 80/20 với `random_state=42` được lưu theo vị trí dòng. Hai tập không trùng vị trí. Trên train, trung vị số trang sản phẩm của nhóm mua và không mua lần lượt là 29 và 16 trang. Trung vị tổng thời gian tương ứng là 1.120,8 và 511,3 giây. Khoảng phân vị 25%–75% của số trang vẫn chồng lấn (15–57 và 6–35 trang). [Notebook EDA](../01_eda.ipynb)

## 2. Phương pháp và lựa chọn mô hình

Pipeline dùng 16 feature và giữ `Revenue` làm nhãn riêng. Loại `PageValues` khỏi cấu hình chính để giảm nguy cơ leakage từ tín hiệu liên quan đến giao dịch. One-hot encode `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType` và `Weekend` với `handle_unknown="ignore"`. Logistic Regression và kNN scale biến số. Các mô hình cây dùng thang số gốc. Mọi bước preprocessing được fit trong phần training của từng fold.

So sánh năm mô hình trên cùng 5 fold từ `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` của tập train. AP là chỉ số chính để chọn mô hình vì lớp mua chỉ chiếm khoảng 15,5% và AP tóm tắt precision theo các mức recall.

| Mô hình | AP trung bình | Độ lệch chuẩn qua 5 fold |
|---|---:|---:|
| Random Forest | **0,3762** | 0,0294 |
| Logistic Regression | 0,3232 | 0,0196 |
| Decision Tree | 0,3180 | 0,0155 |
| kNN | 0,2839 | 0,0217 |
| DummyClassifier | 0,1547 | 0,0002 |

Chọn Random Forest với 100 cây, `max_depth=12`, `min_samples_leaf=5`, `random_state=42` và `class_weight=None`. Trên các xác suất out-of-fold (OOF) của train, chọn ngưỡng tối đa hóa F1 lớp mua. Nếu đồng hạng, chọn ngưỡng cao nhất. F1 OOF đạt 0,4239 tại ngưỡng **0,20964924233624288**, so với 0,0405 tại ngưỡng 0,5. Mô hình, tham số và ngưỡng được chốt trước khi fit lại trên toàn bộ train và đánh giá trên test. [Bảng validation](validation_scores.csv) · [Notebook đánh giá](../03_evaluation.ipynb)

## 3. Kết quả trên tập test

| Chỉ số | Kết quả |
|---|---:|
| Average Precision | **0,3542** |
| ROC-AUC | 0,7610 |
| Precision lớp mua | 0,3030 |
| Recall lớp mua | 0,5838 |
| F1 lớp mua | 0,3989 |

**Confusion matrix** với hàng là nhãn thực tế và cột là dự đoán.

| Thực tế | Không mua | Có mua |
|---|---:|---:|
| Không mua | 1.571 (TN) | 513 (FP) |
| Có mua | 159 (FN) | 223 (TP) |

Mô hình phát hiện 58,38% phiên mua. Trong 736 phiên được dự đoán mua, 223 phiên thực sự mua (30,30%). AP và ROC-AUC dùng xác suất gốc. Precision, Recall, F1 và confusion matrix dùng nhãn ở ngưỡng đã chốt. [Output đánh giá test](../03_evaluation.ipynb)

## 4. Phân tích lỗi

- **159 false negatives.** Trung vị nhóm bỏ sót là 18 trang sản phẩm và 603,7 giây, so với 42 trang và 1.460,9 giây ở nhóm dự đoán đúng phiên mua. Dòng 2.392 (vị trí bắt đầu từ 0 trong CSV) có mua nhưng chỉ xem 3 trang trong 127 giây và nhận điểm mua 0,0180.
- **513 false positives.** Trung vị nhóm báo nhầm là 35 trang và 1.199,9 giây, so với 12 trang và 324,8 giây ở nhóm dự đoán đúng phiên không mua. Dòng 9.576 xem 337 trang trong 11.835,1 giây và nhận điểm mua 0,6187 nhưng không mua.

Các đối chiếu trên mô tả những nhóm lỗi trong test. Chúng cho thấy mức tương tác có thể chồng lấn giữa lớp mua và lớp không mua. [Bảng ví dụ lỗi trong notebook](../03_evaluation.ipynb)

## 5. Giới hạn và kết luận

Kết quả đến từ một split của một dataset có lớp mua thiểu số. Các dòng giống nhau có thể xuất hiện ở nhiều tập do thiếu mã phiên để xác định chúng có phải cùng một phiên hay không. Feature tổng hợp theo phiên có thể cần thông tin chỉ có sau khi phiên kết thúc. Hiệu năng khi dự đoán sớm hoặc áp dụng cho website khác vẫn chưa được xác minh.

Random Forest dẫn đầu trên validation và phát hiện được hơn một nửa số phiên mua trên test tại ngưỡng đã chọn. Với 513 báo nhầm và 159 bỏ sót, lựa chọn ngưỡng cho ứng dụng thực tế còn phụ thuộc chi phí của từng loại lỗi.

## Phụ lục · Thử nghiệm bổ sung trên train

Các thử nghiệm sau dùng 9.864 phiên train. Kết quả test ở mục 3 vẫn áp dụng cho cấu hình và ngưỡng đã chốt ở tuần 3. [Notebook phân tích bổ sung](../04_robustness.ipynb)

### Kiểm tra với grouped cross-validation

Gom các phiên có cùng bộ 16 feature thành 9.773 nhóm. Có 61 nhóm chứa từ hai phiên trở lên. Với `StratifiedKFold`, mỗi fold có từ 21 đến 33 dòng validation trùng vector với phần fit. Với `StratifiedGroupKFold`, số đó bằng 0 ở cả năm fold.

| Mô hình | AP với 5 fold phân tầng | AP với 5 fold phân tầng theo nhóm |
|---|---:|---:|
| Random Forest | 0,3762 ± 0,0294 | 0,3828 ± 0,0203 |
| Logistic Regression | 0,3232 ± 0,0196 | 0,3251 ± 0,0158 |

Random Forest vẫn dẫn đầu trên bộ fold theo nhóm. Chênh lệch AP giữa hai cách chia có thể phản ánh việc thành phần từng fold thay đổi.

### Đánh đổi giữa Precision và Recall

Trên dự đoán out-of-fold theo nhóm của Random Forest cố định, đặt mục tiêu minh họa Precision ít nhất 40% rồi chọn ngưỡng có Recall cao nhất thỏa mốc này. Notebook lưu đường Precision–Recall và vị trí cả hai ngưỡng.

| Phương án | Ngưỡng | Precision | Recall | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| Ngưỡng tuần 3 | 0,209649 | 32,21% | 61,99% | 0,4239 | 1.991 | 580 |
| Ưu tiên Precision | 0,275864 | 40,11% | 38,14% | 0,3910 | 869 | 944 |

Trên các dự đoán OOF này, ngưỡng cao hơn giảm 1.122 báo nhầm và bỏ sót thêm 364 phiên mua. Mức Precision 40,11% được đo trên cùng dự đoán OOF dùng để chọn ngưỡng. Đây là một phương án để minh họa đánh đổi, còn ngưỡng báo cáo test vẫn là ngưỡng tuần 3.

### Tinh chỉnh Random Forest

Thử 12 tổ hợp `max_depth`, `min_samples_leaf` và `class_weight` với nested grouped CV. GridSearchCV chọn theo AP qua 4 fold trong, sau đó cấu hình được đánh giá trên fold ngoài. Trên cùng 5 fold ngoài, AP trung bình là **0,38277** đối với Random Forest cố định và **0,38083** đối với quy trình tinh chỉnh. Chênh lệch trung bình theo cặp là **−0,00193**.

Khi tìm trên toàn bộ train, ứng viên tốt nhất bỏ giới hạn độ sâu, dùng `min_samples_leaf=5` và `class_weight=None`, với AP chọn cấu hình 0,38332. Kết quả trên các fold ngoài chưa cho thấy tinh chỉnh cải thiện AP. Vì vậy, báo cáo giữ cấu hình Random Forest ban đầu cho kết luận chính.

### Learning curve theo nhóm

Giữ nguyên các fold validation theo nhóm và cấu hình Random Forest của tuần 3. Trong mỗi fold, tăng dần tỷ lệ nhóm dùng để fit từ 25% lên 100%. Các dòng cùng nhóm được lấy cùng nhau và tập fit nhỏ nằm trong tập fit lớn hơn.

| Tỷ lệ nhóm fit | Số phiên fit trung bình | AP trung bình ± độ lệch chuẩn |
|---:|---:|---:|
| 25% | 1.972,6 | 0,35310 ± 0,02233 |
| 50% | 3.942,2 | 0,37836 ± 0,02889 |
| 75% | 5.917,0 | 0,37779 ± 0,02338 |
| 100% | 7.891,2 | 0,38277 ± 0,02026 |

AP tăng rõ nhất từ 25% lên 50% nhóm. Từ 50% đến 100%, mức tăng trung bình là 0,00441 và điểm ở mốc 75% thấp hơn nhẹ so với 50%. Đây là kết quả của một cách lấy mẫu lồng nhau trong 5 fold. Hiệu năng với lượng dữ liệu vượt ngoài các mốc đã thử vẫn chưa được xác minh. [Notebook learning curve](../05_learning_curve.ipynb)
