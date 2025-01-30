import cv2  # OpenCV kütüphanesini içe aktar
import pickle  # Python nesnelerini dosyaya kaydedip geri alabilmek için pickle kütüphanesini içe aktar

# 'CarParkPos' dosyasından daha önce kaydedilen koordinatları yüklemeye çalışıyoruz
try:
    with open("CarParkPos", "rb") as f:  # Dosyayı ikili (binary) okuma modunda açıyoruz
        posList = pickle.load(f)  # Dosyadaki veriyi yükleyip posList değişkenine atıyoruz
except:  # Eğer dosya yoksa veya yüklenemiyorsa (hata olursa)
    posList = []  # Boş bir liste oluşturuyoruz (yeni tıklamalar kaydedilecek)

# Park alanlarının genişlik ve yükseklik değerlerindaai belirliyoruz
width = 27  # Dikdörtgenin genişliği
height = 15  # Dikdörtgenin yüksekliği

# Fare tıklama olayını yakalayan fonksiyon
def maouseClick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:  # Sol fare tuşuna tıklanırsa
        posList.append((x, y))  # Tıklanan noktayı posList'e ekliyoruz

    if events == cv2.EVENT_RBUTTONDOWN:  # Sağ fare tuşuna tıklanırsa
        for i, pos in enumerate(posList):  # posList'teki her bir tıklanan noktayı kontrol ediyoruz
            x1, y1 = pos  # x ve y koordinatlarını alıyoruz
            if x1 < x < x1 + width and y1 < y < y1 + height:  # Eğer sağ tıklama, dikdörtgenin içinde ise
                posList.pop(i)  # O noktayı listeden çıkarıyoruz (silme işlemi)

    # Yapılan değişiklikleri 'CarParkPos' dosyasına kaydediyoruz
    with open("CarParkPos", "wb") as f:  # Dosyayı ikili (binary) yazma modunda açıyoruz
        pickle.dump(posList, f)  # Güncellenmiş posList'i dosyaya yazıyoruz

# Sonsuz bir döngü başlatıyoruz, her zaman görseli güncellemek için
while True:
    img = cv2.imread("first_frame.png")  # Görseli okuyoruz (ilk kareyi alıyoruz)

    # Tıklanan her nokta için dikdörtgen çiziyoruz
    for pos in posList:  # posList'teki her koordinat için
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)  # Dikdörtgeni çiziyoruz

    print(posList)  # Tıklanan noktaları terminale yazdırıyoruz

    cv2.imshow("img", img)  # Güncellenen görseli ekranda gösteriyoruz
    cv2.setMouseCallback("img", maouseClick)  # Fare tıklama olaylarını "img" penceresinde dinliyoruz

    cv2.waitKey(1)  # Bir tuşa basılmasını bekliyoruz (1 ms süreyle)

# AŞAMALAR #
'''
1-) Önce while döngüsü kontrolü yapıldı.
2-) Sonra mouseClick fonksiyonu oluşturuldu ve sol tıkla ekleme sağ tık ile silme işlemleri yapıldı.
3-) Yapılan değişiklikleri kaybetmemek adına with open ile dosyayı kayıt ediyoruz.
'''
