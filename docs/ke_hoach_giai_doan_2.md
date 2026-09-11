# Kế hoạch giai đoạn 2

Mục tiêu của giai đoạn 2 là nâng kho mã từ một dự án có cấu trúc tốt thành một hồ sơ kỹ thuật có thể đọc nhanh, chạy lại được và đánh giá được chất lượng nghiên cứu.

## 1. Bổ sung ví dụ lấy dữ liệu công khai

Thêm một nguồn dữ liệu công khai hoặc một lớp tải dữ liệu mẫu để minh họa quy trình lấy dữ liệu, kiểm tra định dạng, làm sạch và đưa vào hệ thống nghiên cứu.

Yêu cầu:
- không dùng dữ liệu tài khoản môi giới;
- không đưa khóa truy cập hoặc dữ liệu có hạn chế công bố;
- dữ liệu mẫu phải đủ để chạy toàn bộ quy trình;
- giữ tách biệt rõ giữa lớp lấy dữ liệu và phần nghiên cứu.

## 2. Hoàn thiện phần huấn luyện và kiểm định mô hình

Bổ sung một ví dụ hoàn chỉnh từ đặc trưng đến mô hình và đánh giá ngoài mẫu.

Quy trình cần thể hiện rõ:
- tạo đặc trưng chỉ từ dữ liệu quá khứ;
- tạo nhãn lợi nhuận tương lai;
- chỉ dùng nhãn khi toàn bộ khoảng tương lai đã quan sát được;
- chia tập dữ liệu theo thời gian;
- huấn luyện theo cửa sổ mở rộng hoặc trượt;
- đánh giá khả năng xếp hạng cổ phiếu trên dữ liệu chưa dùng để huấn luyện.

Không dùng chia ngẫu nhiên cho chuỗi thời gian.

## 3. Tạo báo cáo nghiên cứu mẫu

Thêm một báo cáo sinh tự động từ dữ liệu mẫu hoặc dữ liệu công khai an toàn.

Báo cáo dự kiến gồm:
- số phiên và số mã được sử dụng;
- khoảng thời gian huấn luyện và kiểm định;
- hệ số của mô hình;
- đường giá trị danh mục;
- mức sụt giảm lớn nhất;
- lợi nhuận tích lũy;
- số lần giao dịch;
- chi phí giao dịch;
- tỷ lệ luân chuyển danh mục;
- một số chỉ số đánh giá khả năng xếp hạng.

Kết quả phải được ghi rõ là kết quả minh họa nếu dùng dữ liệu tổng hợp.

## 4. Tạo các hình minh họa kết quả

Sinh các hình trực tiếp từ mã nguồn để người xem không cần đọc toàn bộ chương trình vẫn hiểu được hệ thống.

Các hình chính:
- sơ đồ quy trình nghiên cứu;
- sơ đồ mốc thời gian tín hiệu và khớp lệnh;
- đường giá trị danh mục;
- biểu đồ sụt giảm;
- biểu đồ mức đóng góp của các đặc trưng hoặc hệ số mô hình;
- sơ đồ kiểm tra độ mới của dữ liệu trong phiên.

## 5. Viết tài liệu mô tả mô hình

Tạo một tài liệu ngắn mô tả:
- mục tiêu mô hình;
- đầu vào;
- đầu ra;
- cách huấn luyện;
- cách kiểm định;
- giới hạn;
- các rủi ro sai lệch;
- điều kiện không nên sử dụng kết quả.

Tài liệu phải mô tả đúng phần đã có trong mã nguồn, không quảng cáo hiệu quả vượt quá bằng chứng.

## 6. Cải thiện trang giới thiệu chính

Trang giới thiệu chính sẽ được rút gọn để người đọc trong vài phút có thể hiểu:
- dự án giải quyết bài toán gì;
- quy trình nghiên cứu hoạt động như thế nào;
- điểm kỹ thuật chính nằm ở đâu;
- cách cài đặt;
- cách chạy một ví dụ hoàn chỉnh;
- cách đọc kết quả;
- giới hạn của dự án.

Không đưa giao diện làm việc nội bộ, thông tin tài khoản, dữ liệu riêng hoặc lịch sử nghiên cứu riêng vào kho công khai.

## 7. Củng cố khả năng chạy lại

Mọi ví dụ quan trọng phải có thể chạy lại trên máy mới bằng các lệnh ngắn.

Mục tiêu:
- cài đặt gói;
- chạy kiểm thử;
- chạy ví dụ nghiên cứu;
- sinh báo cáo;
- sinh hình kết quả.

Hệ thống kiểm tra tự động phải tiếp tục chạy trên nhiều phiên bản Python.

## Kết quả mong muốn

Sau giai đoạn 2, người xem kho mã phải có thể xác nhận ba điểm:

1. Dự án có quy trình nghiên cứu định lượng hoàn chỉnh từ dữ liệu đến danh mục và mô phỏng giao dịch.
2. Thiết kế có kiểm soát sai lệch thời gian, chi phí giao dịch, độ mới dữ liệu và chất lượng dữ liệu.
3. Toàn bộ phần công khai có thể chạy lại mà không cần dữ liệu tài khoản hoặc mã nguồn riêng của hệ thống gốc.
