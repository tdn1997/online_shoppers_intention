# Chuẩn bị video và bảo vệ

Bộ slide tiếng Anh có ghi chú trình bày theo từng slide. Mục tiêu diễn tập là **8 phút 30 giây**, dưới giới hạn 10 phút. Thời lượng bên dưới là kế hoạch.

## Phân công và phần nói

| Thành viên | Phần việc | Phần nói |
|---|---|---|
| Nguyễn Duy Thuận (25TX810025) | Chia và lưu train/test, xây dựng pipeline tiền xử lý, huấn luyện và so sánh năm mô hình. Chọn Random Forest theo điểm validation và chọn ngưỡng từ dự đoán out-of-fold trên train. Đánh giá test, phân tích lỗi, tổng hợp báo cáo và chuẩn bị câu hỏi kỹ thuật. | Slide 1, 3, 4, 7, 8 · 5:00 |
| Đoàn Thị Mỹ Thiện (25TX810023) | Đối chiếu nguồn UCI, số phiên, tỷ lệ mua và số liệu EDA giữa notebook 01 với slide 2. Giải thích số trang sản phẩm và thời gian xem của hai nhóm. | Slide 2 · 1:00 |
| Phạm Văn Bình (25TX610001) | Đối chiếu bảng kết quả test và confusion matrix giữa Report và slide 5–6. Giải thích số phiên mua phát hiện đúng, bỏ sót và báo nhầm. Bấm giờ diễn tập, hỗ trợ ghi và kiểm tra video. | Slide 5–6 · 2:30 |

| Slide | Người nói | Nội dung | Thời lượng mục tiêu |
|---|---|---|---:|
| 1 | Thuận | Tên đề tài, thành viên và câu hỏi nghiên cứu | 0:45 |
| 2 | Thiện | Nguồn, đơn vị quan sát, mất cân bằng và EDA | 1:00 |
| 3 | Thuận | Split, feature và preprocessing trong từng fold | 1:00 |
| 4 | Thuận | So sánh mô hình và cách chọn ngưỡng | 1:10 |
| 5 | Bình | Test và cách đọc confusion matrix | 1:25 |
| 6 | Bình | Hai loại lỗi và ví dụ Accuracy của baseline | 1:05 |
| 7 | Thuận | Grouped CV, overfitting và kiểm tra độ nhạy | 1:15 |
| 8 | Thuận | Kết luận, giới hạn và hướng phát triển | 0:50 |

## Câu hỏi ngắn cho Thiện và Bình

**Thiện · Slide 2**

- **Một dòng dữ liệu là gì?** Một phiên truy cập. `Revenue=True` nghĩa là phiên đó kết thúc bằng mua hàng.
- **Dữ liệu có bao nhiêu phiên?** Có 12.330 phiên. Trong đó, 1.908 phiên có mua, chiếm 15,47%.
- **Biểu đồ EDA nói gì?** Trên train, nhóm mua xem trung vị 29 trang sản phẩm, nhóm không mua xem 16 trang. Hai nhóm vẫn có những phiên xem số trang tương tự nhau.

**Bình · Slide 5–6**

- **Kết quả “223 trên 382” nghĩa là gì?** Trong 382 phiên thực sự mua, mô hình nhận ra 223 và bỏ sót 159. Đó là Recall 58,38%.
- **513 báo nhầm là gì?** Đây là các phiên được dự đoán sẽ mua nhưng thực tế không mua.
- **Vì sao luôn đoán không mua đạt khoảng 85%?** Phần lớn phiên thuộc loại không mua. Cách đoán này đúng với nhiều phiên nhưng bỏ sót cả 382 phiên mua. Đồ án dùng Average Precision làm chỉ số chính.

Thuận luyện thêm các câu về fit trong từng fold, cách chọn ngưỡng, `PageValues`, overfitting và grouped CV. Mỗi bạn nên trả lời được bằng lời của mình các câu hỏi về phần đã trình bày.

## Câu hỏi kỹ thuật

1. **Đơn vị dự đoán là gì?** Một phiên truy cập website. `Revenue=True` biểu thị phiên có mua. Feature trong CSV đã được tổng hợp theo phiên.
2. **Vì sao dùng AP?** Chỉ 15,47% phiên trong dữ liệu có mua. Trên test, baseline luôn dự đoán không mua đạt Accuracy 84,51% nhưng phát hiện 0/382 phiên mua. Random Forest phát hiện 223/382 phiên mua tại ngưỡng đã chốt.
3. **Ngăn leakage như thế nào?** Chia train/test có phân tầng, lưu index, fit preprocessing trong mỗi fold và chọn ngưỡng trên dự đoán out-of-fold của train. `PageValues` ở ngoài cấu hình chính vì thời điểm có sẵn chưa xác minh.
4. **Vì sao giữ Random Forest?** Nó dẫn đầu trong so sánh chính với AP validation 0,3762. Với grouped CV, Random Forest cố định đạt 0,38277, còn quy trình tinh chỉnh đạt 0,38083 trên cùng các fold ngoài.
5. **Ngưỡng 0,20965 nghĩa là gì?** Đây là điểm cắt xấp xỉ để gán nhãn mua. Pipeline dùng ngưỡng đầy đủ từ dự đoán out-of-fold, nơi F1 lớp mua cao nhất. AP và ROC-AUC dùng trực tiếp điểm mua.
6. **Có dấu hiệu overfitting không?** Trên 5 fold theo nhóm, AP trung bình trên phần fit là 0,6825, còn validation là 0,3828. Báo cáo dựa vào validation và test để đánh giá khả năng khái quát.
7. **Dòng trùng có ảnh hưởng thế nào?** Có 29 dòng test có vector giống train, đều thuộc lớp không mua. Phép kiểm tra độ nhạy với mô hình và ngưỡng cố định cho AP làm tròn vẫn là 0,3542 khi bỏ tạm các dòng đó. Tập test chính vẫn có đủ 2.466 phiên.
8. **Có thể dùng để dự đoán sớm trong phiên không?** Việc này cần log sự kiện có thứ tự thời gian để dựng feature tại mốc ra quyết định. Hiện tại mô hình được đánh giá offline trên đặc trưng tổng hợp theo phiên.

## Xác minh trước khi nộp

- [x] Chia phần nói cho ba thành viên. Mỗi người có ít nhất một slide nội dung.
- [ ] Diễn tập toàn bộ, đo thời lượng thực tế và giữ dưới hoặc bằng 10 phút.
- [ ] Ghi video trước, mở lại để kiểm tra tiếng, hình và quyền xem.
- [ ] Ghi đường dẫn video, thời lượng và ngày kiểm tra vào hồ sơ nộp.
- [ ] Có mặt khi báo cáo và lưu bằng chứng tham gia nếu môn học yêu cầu.
- [ ] Hoàn thành Peer Assessment theo kênh môn học khi áp dụng.

| Bằng chứng | Nhóm điền sau khi hoàn thành |
|---|---|
| Người trình bày và số slide phụ trách | |
| Ngày diễn tập và thời lượng thực tế | |
| Đường dẫn video và ngày kiểm tra quyền xem | |
| Tình trạng phiếu Peer Assessment | |
| Ngày báo cáo và phần tham gia của từng người | |
