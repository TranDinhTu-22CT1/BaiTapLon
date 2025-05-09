from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytesseract
from PIL import Image, ImageOps
from io import BytesIO
import schedule
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Python\checkphatnguoi\tesseract\tesseract.exe'

def get_captcha_text(driver):
    try:
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "imgCaptcha"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", captcha_element)

        location = captcha_element.location_once_scrolled_into_view
        size = captcha_element.size

        screenshot = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))

        window_size = driver.execute_script("return [window.innerWidth, window.innerHeight];")
        screenshot_size = img.size

        scale_x = screenshot_size[0] / window_size[0]
        scale_y = screenshot_size[1] / window_size[1]

        left = int(location['x'] * scale_x)
        top = int(location['y'] * scale_y)
        right = int((location['x'] + size['width']) * scale_x)
        bottom = int((location['y'] + size['height']) * scale_y)

        captcha_img = img.crop((left, top, right, bottom))

        captcha_img = captcha_img.convert("L")
        captcha_img = ImageOps.invert(captcha_img)
        captcha_img = ImageOps.autocontrast(captcha_img)
        captcha_img = captcha_img.point(lambda x: 0 if x < 150 else 255, '1')
        captcha_img = captcha_img.resize((captcha_img.width * 3, captcha_img.height * 3), Image.LANCZOS)

        configs = [
            '--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789',
            '--psm 7 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789',
            '--psm 6 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'
        ]

        for config in configs:
            text = pytesseract.image_to_string(captcha_img, config=config).strip().lower()
            text = ''.join(filter(str.isalnum, text))
            if len(text) == 6:
                print(f"Thành công: {text}")
                return text
            else:
                print(f"Thất bại ({config}): {text}")

        return None

    except Exception as e:
        print(f"Lỗi khi xử lý captcha: {e}")
        return None

def tra_cuu_phat_nguoi(bien_so, loai_xe):
    print(f"\n==> [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Đang tra cứu biển số: {bien_so}")
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")

    try:
        attempts = 0
        while attempts < 10:
            attempts += 1
            print(f"Thử lần thứ {attempts}")
            driver.refresh()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).send_keys(bien_so)

            select_loai_xe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LoaiXe")))
            for option in select_loai_xe.find_elements(By.TAG_NAME, 'option'):
                if option.text.strip() == loai_xe.strip():
                    option.click()
                    break

            captcha_text = get_captcha_text(driver)
            if not captcha_text or len(captcha_text) < 4:
                print("Captcha này khó nhìn quá. Đang thử lại...")
                continue

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "txt_captcha"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "txt_captcha"))).send_keys(captcha_text)
            driver.find_element(By.CLASS_NAME, "btnTraCuu").click()

            try:
                container = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "bodyPrint123"))
                )
                content = container.text.strip()
                if "Biển kiểm soát" in content and "Thời gian vi phạm" in content:
                    print("Tìm thấy thông tin vi phạm!")
                    time.sleep(5)
                    break
                else:
                    print("Sai captcha hoặc không có dữ liệu.")
                    time.sleep(3)
                    continue
            except:
                continue
    finally:
        driver.quit()

def job():
    tra_cuu_phat_nguoi("23A14482", "Ô tô")

if __name__ == "__main__":
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("12:00").do(job)

    print("Đang chạy và chờ đến 6h hoặc 12h để kiểm tra phạt nguội...")
    while True:
        schedule.run_pending()
        time.sleep(1)
