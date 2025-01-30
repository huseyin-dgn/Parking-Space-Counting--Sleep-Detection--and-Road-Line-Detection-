import cv2
import numpy as np

def region_of_interest(image, vertices):
    """
    Görüntünün sadece belirli bir bölgesini işlemek için maske uygular.
    - image: İşlenecek görüntü.
    - vertices: Maske uygulanacak bölgenin köşe koordinatları [(x1, y1), (x2, y2), ...].
    """
    mask = np.zeros_like(image)  # Görüntüyle aynı boyutta siyah bir maske oluşturulur.
    match_mask_color = 255  # Maske rengi beyaz olarak ayarlanır (gri tonlamada en parlak değer).
    cv2.fillPoly(mask, vertices, match_mask_color)  # Belirtilen köşelere göre maske doldurulur.
    masked_img = cv2.bitwise_and(image, mask)  # Orijinal görüntü ve maske birleştirilir.
    return masked_img

def drawLine(image, lines):
    """
    Tespit edilen çizgileri görüntüye çizer.
    - image: Orijinal görüntü.
    - lines: Çizgilerin başlangıç ve bitiş noktalarını içeren bir liste.
    """
    image = np.copy(image)  # Orijinal görüntü kopyalanır.
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)  # Siyah arka plan.

    if lines is not None:  # Eğer çizgiler varsa:
        for line in lines:  # Her bir çizgi için döngü.
            for x1, y1, x2, y2 in line:  # Çizginin başlangıç ve bitiş noktaları.
                cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), 10)  # Çizgi çizilir (yeşil, kalınlık=10).

    # Orijinal görüntü ve çizgiler birleştirilir (alpha blending ile).
    image = cv2.addWeighted(image, 0.8, blank_image, 1, 0.0)
    return image

def process(image):
    """
    Görüntüyü işleyerek çizgileri tespit eder ve çizer.
    - image: İşlenecek görüntü.
    """
    height, width = image.shape[0], image.shape[1]  # Görüntünün yüksekliği ve genişliği alınır.

    # 1. Adım: ROI (Region of Interest) için üçgen alan tanımlanır: Alt köşeler ve orta üst.
    region_of_interest_ver = [(0, height), (width / 2, height / 2), (width, height)]

    # 2. Adım: Görüntüyü gri tonlamaya çeviririz.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Görüntü gri tonlamaya çevrilir.

    # 3. Adım: Canny kenar tespiti uygulanır.
    canny_image = cv2.Canny(gray_image, 250, 120)  # Kenar tespiti yapılır. (minVal=250, maxVal=120)

    # 4. Adım: Belirlenen bölge dışındaki alanlar kaldırılır.
    cropped_img = region_of_interest(canny_image, np.array([region_of_interest_ver], np.int32))

    # 5. Adım: Hough dönüşümüyle çizgiler tespit edilir.
    lines = cv2.HoughLinesP(cropped_img, rho=2, theta=np.pi/180, threshold=220, minLineLength=10, maxLineGap=5)
    # rho=2: Çözünürlük (2 piksel).
    # theta=np.pi/180: Açısal çözünürlük (1 derece).
    # threshold=220: Çizgi tespiti için gereken minimum oy.
    # minLineLength=10: Tespit edilecek en kısa çizgi uzunluğu.
    # maxLineGap=5: İki segment arasındaki maksimum boşluk.

    # 6. Adım: Çizgiler görüntüye çizilir.
    imageWithLine = drawLine(image, lines)
    return imageWithLine

# Video dosyası okunur.
cap = cv2.VideoCapture("video1.mp4")

while True:
    # Her bir kareyi okuruz.
    success, img = cap.read()
    if not success:  # Eğer kare okunamadıysa (video bitti), döngüden çıkarız.
        break

    # Kareyi işlemden geçiririz.
    processed_img = process(img)

    # İşlenmiş görüntüyü gösteririz.
    cv2.imshow("Processed Image", processed_img)

    # 'q' tuşuna basılırsa döngü sona erer.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Video ve pencereler serbest bırakılır.
cap.release()
cv2.destroyAllWindows()

# -- UYGULAMA AÇIKLAMALARI -- #
'''
1-) ROI (Region of Interest) tanımlama:
Görüntünün ilgilenilen bölgesi belirleniyor. Üçgen bir alan seçiliyor.

2-) Görüntünün gri tonlamaya çevrilmesi:
cv2.cvtColor ile görüntü gri tonlamaya dönüştürülüyor.

3-) Canny kenar algılama:
Kenar tespiti yapmak için cv2.Canny kullanılıyor.

4-) Maskelenmiş görüntü oluşturma:
Tanımlanan ROI bölgesine uygun bir maske uygulanarak, sadece istenen alan işleniyor.

5-) Hough dönüşümüyle çizgilerin tespiti:
Hough dönüşümü kullanılarak kenar algılamadan elde edilen verilerle çizgiler tespit ediliyor.

6-) Çizgilerin görüntüye çizilmesi:
Tespit edilen çizgiler, görüntünün üzerine çiziliyor (cv2.line ile).

7-) Görüntülerin işlenmesi ve gösterilmesi:
Videonun her bir karesi bu işlemlerden geçirilerek işleniyor ve ekrana gösteriliyor.
'''

'''
İşlem Adımları
process Fonksiyonu Başlar:

- Region of Interest (ROI) Tanımı: Görüntünün işlenecek bölgesinin koordinatları belirlenir (region_of_interest_ver).
- Gri Tonlama (Gray Conversion): Görüntü gri tonlamaya çevrilir (cv2.cvtColor).
- Canny Kenar Algılama: Gri tonlamalı görüntü üzerinde kenar tespiti yapılır (cv2.Canny).
- Region of Interest Uygulaması: Yukarıda tanımlanan region_of_interest fonksiyonu burada çağrılır.
region_of_interest Fonksiyonu Çalışır:

Maske İşlemi: Görüntünün sadece istenen bölgesi işlenir, diğer alanlar siyah maske ile kapatılır (cv2.fillPoly).
Hough Çizgi Algılama:

Maske uygulanmış görüntüye Hough dönüşümü uygulanır ve çizgiler algılanır (cv2.HoughLinesP).
Çizgileri Çizme:

Algılanan çizgiler, drawLine fonksiyonu kullanılarak orijinal görüntü üzerine çizilir.
'''