import cv2
import numpy as np
import pickle

# Park alanlarını kontrol eden fonksiyon
def chechParkSpace(image):
    spaceCounter = 0  # Boş park alanlarının sayısını tutan sayaç

    # Her bir park alanının koordinatlarını kontrol et
    for pos in posList:
        x, y = pos  # Pos listesi her bir park alanının (x, y) koordinatını içeriyor

        img_cropp = image[y: y + height, x: x + width]  # Park alanını (dikdörtgen şeklinde) kesiyoruz
        count = cv2.countNonZero(img_cropp)  # Kesilen alandaki beyaz pikselleri sayıyoruz

        print(count)  # Piksel sayısını ekrana yazdırıyoruz

        # Eğer beyaz piksel sayısı 150'den küçükse, boş park yeri olarak kabul edilir
        if count < 150:
            color = (0, 255, 0)  # Yeşil (boş)
            spaceCounter += 1  # Boş park yeri sayısını artırıyoruz
        else:
            color = (0, 0, 255)  # Kırmızı (dolu)

        # Park alanının etrafını dikdörtgenle çiziyoruz
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)

        # Piksel sayısını park alanının içine yazıyoruz
        cv2.putText(img, str(count), (x, y + height - 2), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

        # Toplam boş park yerini ekranın üst kısmına yazıyoruz
    cv2.putText(img, f"Free : {spaceCounter}/ {len(posList)}", (15, 24), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 3)


# Dikdörtgenin genişliği ve yüksekliği

width = 27
height = 15

# Video kaynağını açıyoruz
cap = cv2.VideoCapture("video.mp4")  # 'video.mp4' yerine kamerayı da kullanabilirsin (örneğin: 0)

# Önceden kaydedilmiş park yerlerinin koordinatlarını yüküyoruz
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)  # 'CarParkPos' dosyasından park yerlerinin koordinatlarını alıyoruz

# Video kareleri üzerinde döngü başlatıyoruz
while True:
    succes, img = cap.read()  # Videodan bir kare okuyoruz
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Görüntüyü gri tonlamaya çeviriyoruz
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)  # Görüntüyü bulanıklaştırıyoruz
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # Adaptive thresholding ile görüntüyü siyah/beyaz yapıyoruz
    # imgBlur: Bulanıklaştırılmış gri tonlamalı görüntü
    # 255: Beyaz rengi temsil eden değer
    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C: Ağırlıklı ortalama kullanarak adaptif eşikleme
    # cv2.THRESH_BINARY_INV: Siyah beyaz yapma, tersine çevirme
    # 25: Kare boyutu (yaklaşık olarak bir piksel bölgesi)
    # 16: C parametresi, eşik değerinden çıkacak sabit fark

    imgMedian = cv2.medianBlur(imgThreshold, 5)  # Median filtreleme yapıyoruz (gürültü azaltma)
    imgDilate = cv2.dilate(imgMedian, np.ones((3, 3), np.uint8), iterations=2)  # Görüntüyü büyütüyoruz (dilasyon)

    chechParkSpace(imgDilate)  # Park yerlerini kontrol etme fonksiyonunu çağırıyoruz

    cv2.imshow("img", img)  # Orijinal görüntüyü ekranda gösteriyoruz
    # Opsiyonel olarak median filtreyi de gösterebiliriz
    # cv2.imshow("imgMedian", imgMedian)

    # Her bir kareyi ekranda 200ms gösteriyoruz
    cv2.waitKey(200)  # 200ms bekle, her bir kareyi göster
