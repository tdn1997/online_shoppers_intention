# Dữ liệu Online Shoppers Purchasing Intention

Dataset của Sakar và Kastro (2018) gồm **12.330 phiên truy cập**. Mỗi dòng mô tả một phiên và có 17 biến đầu vào cùng nhãn **`Revenue`**. `TRUE` biểu thị phiên có mua hàng. Có 1.908 phiên mua (15,47%) và 10.422 phiên không mua. Giấy phép CC BY 4.0. [UCI Machine Learning Repository](https://doi.org/10.24432/C5F88Q)

## Biến đầu vào và nhãn

| Biến | Kiểu sử dụng và ý nghĩa |
|---|---|
| `Administrative`, `Informational`, `ProductRelated` | Số trang hành chính, thông tin và sản phẩm được xem trong phiên. |
| `Administrative_Duration`, `Informational_Duration`, `ProductRelated_Duration` | Tổng thời gian trên từng nhóm trang, tính bằng giây. |
| `BounceRates`, `ExitRates` | Chỉ số tỷ lệ thoát do hệ thống phân tích web ghi nhận. |
| `PageValues` | Giá trị trang liên quan đến giao dịch. Phân tích riêng trong notebook 06 vì thời điểm có sẵn của biến chưa được xác minh. |
| `SpecialDay` | Mức độ gần với một dịp mua sắm đặc biệt. |
| `Month`, `Weekend` | Tháng truy cập và cờ cuối tuần. |
| `OperatingSystems`, `Browser`, `Region`, `TrafficType` | Mã danh mục hệ điều hành, trình duyệt, vùng và nguồn truy cập. |
| `VisitorType` | Loại khách, ví dụ khách mới hoặc khách quay lại. |
| `Revenue` | Nhãn nhị phân. Lớp dương là phiên có mua hàng. |

## Tệp và cách sử dụng

- [online_shoppers_intention.csv](online_shoppers_intention.csv) là CSV gốc. Có 0 giá trị thiếu và 125 dòng trùng hoàn toàn sau lần xuất hiện đầu tiên. Giữ toàn bộ dòng vì CSV thiếu mã phiên để phân biệt các phiên có cùng giá trị tổng hợp.
- [split_indices.json](split_indices.json) lưu vị trí dòng của 9.864 phiên train và 2.466 phiên test sau khi chia phân tầng 80/20 với seed 42. Notebook kiểm tra SHA-256 của CSV trước khi đọc split. Giữ thứ tự dòng và byte của CSV khi chạy lại.
- Cấu hình chính tách `Revenue` khỏi feature và bỏ `PageValues`, còn 16 biến. Dữ liệu theo hàng đã tổng hợp cả phiên nên kết quả mô tả phân loại offline.
