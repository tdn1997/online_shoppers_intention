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

### Độ bất định của kết quả

Ước lượng khoảng bootstrap 95% với 2.000 lượt lấy mẫu có hoàn lại trên 2.454 nhóm test. Mỗi nhóm gồm các phiên có cùng bộ 16 feature. Giữ mô hình và ngưỡng cố định ở mọi lượt lấy mẫu.

| Chỉ số | Kết quả test | Khoảng bootstrap 95% |
|---|---:|---:|
| Average Precision | 0,3542 | 0,3101–0,4053 |
| Precision lớp mua | 30,30% | 26,94–33,65% |
| Recall lớp mua | 58,38% | 53,20–63,23% |

Các khoảng này mô tả biến động khi lấy mẫu lại test với giả định các nhóm độc lập. Độ biến động khi huấn luyện trên dữ liệu khác hoặc chuyển sang website khác vẫn chưa được xác minh. [Notebook tính khoảng bootstrap](../06_model_review.ipynb) · [Phương pháp bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)

## 4. Phân tích lỗi

- **159 false negatives.** Trung vị nhóm bỏ sót là 18 trang sản phẩm và 603,7 giây, so với 42 trang và 1.460,9 giây ở nhóm dự đoán đúng phiên mua. Dòng 2.392 (vị trí bắt đầu từ 0 trong CSV) có mua nhưng chỉ xem 3 trang trong 127 giây và nhận điểm mua 0,0180.
- **513 false positives.** Trung vị nhóm báo nhầm là 35 trang và 1.199,9 giây, so với 12 trang và 324,8 giây ở nhóm dự đoán đúng phiên không mua. Dòng 9.576 xem 337 trang trong 11.835,1 giây và nhận điểm mua 0,6187 nhưng không mua.

Các đối chiếu trên mô tả những nhóm lỗi trong test. Chúng cho thấy mức tương tác có thể chồng lấn giữa lớp mua và lớp không mua. [Bảng ví dụ lỗi trong notebook](../03_evaluation.ipynb)

## 5. Giới hạn và kết luận

Kết quả đến từ một split của một dataset có lớp mua thiểu số. Có 29 phiên test có vector 16 feature trùng với ít nhất một phiên train. CSV thiếu mã phiên để xác định chúng là bản sao hay các phiên khác nhau có cùng giá trị tổng hợp. Một số feature tổng hợp có thể cần dữ liệu tới cuối phiên. Hiệu năng khi dự đoán sớm hoặc áp dụng cho website khác vẫn chưa được xác minh. [Kiểm tra trùng vector](../06_model_review.ipynb)

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

### Kiểm tra bộ feature và mô hình boosting

Dùng cùng 5 fold theo nhóm trên train và tính AP trung bình qua fold. Mỗi fold dùng nhóm xác định từ 16 feature chính cho mọi cấu hình.

| Cấu hình | AP trung bình ± độ lệch chuẩn |
|---|---:|
| Random Forest · 16 feature chính | 0,38277 ± 0,02026 |
| Random Forest · thêm `PageValues` | 0,74265 ± 0,01810 |
| Random Forest · 8 biến ngữ cảnh | 0,26739 ± 0,01231 |
| HistGradientBoosting · 16 feature chính | 0,35902 ± 0,02126 |

`PageValues` là chỉ số giá trị trang liên quan đến giao dịch. Mức tăng AP cho thấy mô hình có thể khai thác mạnh thông tin của cột này. Để xác định có leakage hay không, cần biết giá trị được tính từ dữ liệu của giai đoạn nào và có sẵn khi dự đoán hay chưa. Cấu hình báo cáo chính dùng 16 feature vì thời điểm có sẵn của `PageValues` chưa được xác minh. [Mô tả dữ liệu UCI](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)

Bộ 8 biến ngữ cảnh gồm `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType`, `Weekend` và `SpecialDay`. So sánh này đo tác động của việc bỏ các biến tổng hợp hành vi. Đánh giá dự đoán sau ba lượt xem trang cần timestamp và chuỗi sự kiện trong phiên để dựng feature tại thời điểm đó. CSV hiện tại chỉ có dữ liệu tổng hợp theo phiên. [Nghiên cứu về dự đoán sớm trong phiên](https://link.springer.com/article/10.1007/s12525-020-00448-x)

Cấu hình HistGradientBoosting được thử với 100 vòng boosting, `learning_rate=0.1` và `max_leaf_nodes=31`, dùng hỗ trợ biến phân loại theo dtype. Cấu hình này có AP thấp hơn Random Forest trên cùng fold. Kết luận giới hạn ở cấu hình đã thử. [Notebook so sánh](../06_model_review.ipynb) · [Tài liệu HistGradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html)

### Calibration của điểm mua

So sánh điểm Random Forest gốc với điểm sau calibration sigmoid. Bộ hiệu chỉnh được học trong 4 fold nhóm nội bộ của từng fold ngoài. Bảng dưới tính trên dự đoán OOF của 5 fold ngoài. Baseline dùng tỷ lệ phiên mua của phần fit cho mọi phiên validation trong fold tương ứng.

| Phương án | Brier loss ↓ | Log loss ↓ |
|---|---:|---:|
| Random Forest gốc | 0,11315 | 0,36059 |
| Calibration sigmoid | 0,11361 | 0,36560 |
| Tỷ lệ mua phần fit | 0,13077 | 0,43078 |

Ở nhóm điểm cao nhất của Random Forest gốc, điểm trung bình là 33,10% và tỷ lệ mua quan sát là 36,64%. Sau sigmoid, các số tương ứng ở nhóm điểm cao nhất là 38,27% và 36,59%. Sigmoid thu hẹp chênh lệch tuyệt đối ở nhóm này, nhưng cả hai loss tính trên toàn bộ OOF đều tăng nhẹ. Demo dùng điểm gốc để xếp hạng và gán nhãn tại ngưỡng tuần 3. [Biểu đồ calibration](../06_model_review.ipynb) · [Tài liệu hiệu chỉnh xác suất](https://scikit-learn.org/stable/modules/calibration.html)
