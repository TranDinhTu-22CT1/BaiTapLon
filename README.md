# BaiTapLon
Bài tập tự động tra cứu phạt nguội

Những thư viện được sử dụng:
- Selenium
- webdriver-manager
- Pillow
- pytesseract
- schedule

Các bước hoạt động của code
1. Mở trình duyệt Chrome
2. Truy cập trang web https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html
3. Nhập biển số và chọn loại xe
4. Tải ảnh CAPTCHA
5. Tiền xử lý ảnh bằng Pillow: chuyển sang đen trắng, đảo màu, tăng tương phản, resize
6. Dùng pytesseract với nhiều cấu hình để đọc CAPTCHA
7. Gửi form và kiểm tra kết quả
8. Lặp lại tối đa 10 lần nếu CAPTCHA sai hoặc không có kết quả
9. sau khi tìm được mã captcha và hiển thị thông tin vi phạm thì sẽ tự động dừng chương trình, chờ đến giờ tiếp theo

Những Thứ cần cài đặt
- cài đặt thư viện trong file requirements.txt: pip install requirements.txt
- cài đặt Tesseract OCR (đã có 1 file trong thư mục tesseract1, chỉ cần chạy file rồi lấy đường dẫn đến thư mục đã cài đặt)
Sau khi cài đặt xong các thư viện thì chỉ cần chạy chương trình nữa là hoàn tất


