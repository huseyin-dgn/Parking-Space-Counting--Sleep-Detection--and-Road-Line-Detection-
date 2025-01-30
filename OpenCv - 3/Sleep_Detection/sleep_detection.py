import cv2
import cvzone
import mediapipe as mp
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import tkinter as tk
from tkinter import messagebox

from typing_extensions import runtime

# Video dosyasını açıyoruz
cap = cv2.VideoCapture(0)

# Mediapipe FaceMeshDetector kullanıyoruz
detector = FaceMeshDetector()

# Canlı grafik için bir plot oluşturuyoruz, Y ekseninde göz kırpma oranını göstereceğiz
plotY = LivePlot(540, 360, [10, 60])

# Yüzdeki belirli noktaların indekslerini içeren
# (göz ve ağız noktalarına yakın)
idList = [22, 23, 24, 26, 110, 157, 159, 161, 130, 243]

# Çizim için başlangıç rengi kırmızı
color = (0, 0, 255)

# Göz kırpma oranlarını tutmak için bir liste
ratioList = []
# Göz kırpma sayısını tutan sayaç
counter = 0
# Göz kırpma tespit sayısını tutan sayaç
blickCounter = 0

# Sonsuz döngü başlatıyoruz, her bir kareyi analiz edeceğiz
while True:
    succes, img = cap.read()

    # Yüzün mesh modelini buluyoruz, 'draw=False' ile yüz hatlarını çizdirmiyoruz
    img, faces = detector.findFaceMesh(img, draw=False)

    # Eğer yüz algılanırsa
    if faces:
        face = faces[0]  # İlk yüzü alıyoruz

        # idList'teki her nokta için yüz üzerinde küçük daireler çiziyoruz
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)  # 5 piksel çapında kırmızı daireler

        # Göz kırpma tespiti için yüzün belirli noktalarını alıyoruz
        leftUp = face[159]  # Sol üst göz noktası
        leftDown = face[23]  # Sol alt göz noktası
        leftLeft = face[130]  # Sol gözün dış noktası
        leftRight = face[243]  # Sol gözün iç noktası

        # Yükseklik (dikey mesafe) ve genişlik (yatay mesafe) arasındaki mesafeyi hesaplıyoruz
        lenghVar, _ = detector.findDistance(leftUp, leftDown)  # Dikey mesafe
        lenghHor, _ = detector.findDistance(leftLeft, leftRight)  # Yatay mesafe

        # Çizim için yeşil ve mavi renklerde çizgiler çiziyoruz
        cv2.line(img, leftUp, leftDown, (0, 255, 0), 3)  # Dikey çizgi
        cv2.line(img, leftLeft, leftRight, (255, 255, 0), 3)  # Yatay çizgi

        # Yüzdeki göz orantısını hesaplıyoruz
        ratio = (lenghVar / lenghHor) * 100  # Yükseklik/genişlik oranı
        ratioList.append(ratio)  # Oranı listeye ekliyoruz

        # Eğer oran listesinde 3'ten fazla değer varsa, eski değeri çıkarıyoruz
        if len(ratioList) > 3:
            ratioList.pop(0)

        # Ortalama oranı hesaplıyoruz
        ratioAvg = sum(ratioList) / len(ratioList)
        print(ratioAvg)  # Oranı ekrana yazdırıyoruz

        # Eğer oran %35'ten küçükse ve henüz bir göz kırpma tespiti yapılmadıysa
        if ratioAvg < 35 and counter == 0:
            blickCounter += 1  # Göz kırpma sayısını artırıyoruz
            color = (0, 255, 0)  # Göz kırpma tespit edilince rengi yeşil yapıyoruz
            counter = 1  # Sayaç başlatılıyor

        # Eğer bir göz kırpma tespiti yapıldıysa
        if counter != 0:
            counter += 1  # Sayaç artıyor
            # Eğer sayaç 10'dan büyükse, tekrar sıfırlıyoruz
            if counter > 10:
                counter = 0
                color = (0, 0, 255)  # Rengi kırmızıya geri alıyoruz

        # Göz kırpma sayısını ekranda gösteriyoruz
        cvzone.putTextRect(img, f'BlickCount: {blickCounter}', (50, 100), colorR=color)

        #if blickCounter > 5:
          #  messagebox.showerror(
               # "Threading Error",
                #"Çok fazla göz kırpma t4spit edildi lütfen uyunuz."
           # )


        # Orta grafiği güncelliyoruz ve renkleri ayarlıyoruz
        imgPlot = plotY.update(ratioAvg, color)

        # Görüntüyü yeniden boyutlandırıyoruz
        img = cv2.resize(img, (640, 400))

        # Görüntü ve grafiklerin birleştiği bir ekran oluşturuyoruz
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        img_stack= cv2.resize(imgStack , (900 , 500))

    # Sonuçları ekranda gösteriyoruz
    cv2.imshow("img", img_stack)

    # 25 ms bekliyoruz ve herhangi bir tuşa basılırsa döngüyü sonlandırıyoruz
    cv2.waitKey(25)

