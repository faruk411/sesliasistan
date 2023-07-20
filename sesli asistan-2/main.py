
from playsound import playsound #ses çalmak için kullanılan modül
import speech_recognition as sr #bir ses dosyasını veya mikrofondan aldığı sesi yazı ve ya sesli olarak geri dönüş yapmayı sağlar
from gtts import gTTS #metni konuşmaya dönüştürmek için kullanılan modül
import os
import webbrowser # internet tarayıcısını kullanarak internet sitelerini açabilmemizi sağlar
from datetime import datetime #zamanı kullanmamızı sağlayan modül
import requests #internetten veri çekmeyi sağlar
from bs4 import BeautifulSoup #çektiğimiz veriyi çözümler
from googletrans import Translator #google çerivi için
import random  # rastgele seçimler yapacağımız şeyler için kullanıyoruz
import time  # seyirde can takibi güç takibi kolay olsun diye
import abc
from ursina import * #oyun tasarımı için
from ursina.prefabs.first_person_controller import FirstPersonController #oyun kontrolü
#import pygame
#from selenium import webdriver
#import pyaudio

r=sr.Recognizer()
class Sesliasistan:
    #sesli asistandaki ses fonksiyonu
    def seslendirme(self,metin):
        xtts=gTTS(text=metin,lang="tr",slow=False)
        dosya="answer.mp3"
        xtts.save(dosya)
        playsound(dosya)
        os.remove(dosya)
    #ingilizce çeviri için ses fonksiyonu
    def ses(self,soz):
        x=gTTS(text=soz,lang="en",slow=False)
        dos="answer.mp3"
        x.save(dos)
        playsound(dos)
        os.remove(dos)
    #mikrofondaki sesi alıp kaydettiğimiz fonksiyon
    def ses_kayit(self):
        with sr.Microphone() as kaynak:
            audio=r.listen(kaynak)
            voice=""
            try:
                voice=r.recognize_google(audio,language="tr-TR")
            except sr.UnknownValueError:
                print("anlayamadım")
            return voice


    #mikrofandan alınan sese göre asistanın karşılık verdiği fonksiyon
    def ses_karsilik(self,gelenses):

        if "nasılsın" in gelenses:
            self.seslendirme("iyiyim sen nasılsın")

        elif "saat kaç" in gelenses:
            self.seslendirme(datetime.now().strftime("%H:%M:%S"))
        elif "youtube aç" in gelenses:
            veri=self.ses_kayit()
            url="https://www.youtube.com/search?q".format(veri)
            webbrowser.get().open(url)
            self.seslendirme("youtube açıldı")
        elif "kendini kapatabilirsin" in gelenses:
            self.seslendirme("görüşürüz Allaha emanet ")
            exit()

        elif "arama yapar mısın" in gelenses:
            try:
                self.seslendirme("ne aramamı istiyorsun")
                veri=self.ses_kayit()
                url="https://www.google.com/search?q="+veri
                webbrowser.get().open(url)
                self.seslendirme(veri + "için bulduğum sonuçlar")
            except:
                self.seslendirme("internet bağlantısı yok ")

        elif "disney aç" in gelenses:
            self.seslendirme("disney açılıyor")
            veri=self.ses_kayit()
            url="https://www.disneyplus.com/tr-tr/home"+veri
            webbrowser.get().open(url)

        elif "e-devleti açarmısın" in gelenses or "e-devlet aç" in gelenses:
            veri = self.ses_kayit()
            self.seslendirme("e devlet açılıyor")
            url="https://www.turkiye.gov.tr".format(veri)
            webbrowser.get().open(url)
        if "hangi gündeyiz" in gelenses:
            today=time.strftime("%A")
            today.capitalize()
            if today=="Monday":
                today="Pazartesi"
            elif today=="Tuesday":
                today="Salı"
            elif today=="Wednesday":
                today="Çarşamba"
            elif today=="Thursday":
                today="Perşembe"
            elif today=="Friday":
                today="Cuma"
            elif today=="Saturday":
                today="Cumartesi"
            elif today=="Sunday":
                today="Pazar"
            self.seslendirme(today)
        elif "steam açar mısın" in gelenses:
            self.seslendirme("steam açılıyor")
            os.startfile("C:\Program Files (x86)\Steam\steam.exe")

        elif "görüntü açar mısın" in gelenses:
            self.seslendirme("diskord açılıyor")
            os.startfile("C:\Discord\dis\Discord.exe")
        elif "hava durumunu söyler misin" in gelenses or "hava durumu" in gelenses:
            self.seslendirme("hangi şehrin hava durumunu istersiniz")
            veri=self.ses_kayit()
            request=requests.get("https://www.ntvhava.com/{}-hava-durumu".format(veri))
            html=request.content
            soup=BeautifulSoup(html,"html.parser")
            gu=soup.find_all("div",{"class":"daily-report-tab-content-pane-item-box-bottom-degree-big"})
            ge=soup.find_all("div",{"class":"daily-report-tab-content-pane-item-box-bottom-degree-small"})
            ha=soup.find_all("div",{"class":"daily-report-tab-content-pane-item-text"})
            gunduz=[]
            gece=[]
            hava=[]
            for x in gu:
                x=x.text
                gunduz.append(x)
            for y in ge:
                y=y.text
                gece.append(y)
            for z in ha:
                z=z.text
                hava.append(z)
            self.seslendirme("{} için yarınki hava durumu şöyle,{} gündüz sıcaklığı {} gece sıcaklığı {}".format(veri,hava[0],gunduz[0],gece[0]))

        elif "fıkra anlat" in gelenses or "fıkra anlatır mısın" in gelenses:
            self.seslendirme("tamam anlatırım")
            liste=["Adamın biri kitap okurken ölmüş neden? Çünkü satır başına gelmiş.","adamın biri yolda gelene geçene su atıyormuş,çünkü adamın adı suatmış"
                   ,"Adam, eve zil zurna sarhoş gelmiş ve karısına bakarak;  Ne kadar çirkinsin, demiş. Karısı; Sen de pis sarhoşun tekisin, deyince, adam da; İyi de benimki sabaha geçecek!"
                   ,"Adamın biri var mış hakem gelip bakmış",""]
            rastgele=random.choice(liste)
            self.seslendirme(rastgele)

        #ceviri yapar
        elif "çeviri yap" in gelenses:
            self.seslendirme("hangi dile çevirmemi istersin")
            veri=self.ses_kayit()
            print(veri)
            if "İngilizce" in veri:
                self.seslendirme("hangi cümle veya kelime çevirmemi istersin")
                veri1 = self.ses_kayit()
                veri2 = []
                veri2.append(veri1)
                translator = Translator()
                ceviri = translator.translate("{}".format(veri2), src='tr', dest='en')
                print(ceviri.text)
                self.ses(ceviri.text)

            if "Türkçe" in veri:
                self.seslendirme("hangi cümle veya kelimeyi cevirmemi istersin")
                veri1 = self.ses_kayit()
                veri2 = []
                veri2.append(veri1)
                translator = Translator()
                ceviri = translator.translate("{}".format(veri2), src='en', dest='tr')
                print(ceviri.text)
                self.seslendirme(ceviri.text)
        elif "hesaplama yap" in gelenses:
            self.seslendirme("hangi işlem yapmak istiyorsun")
            veri=self.ses_kayit()
            if "toplama" in veri:
                self.seslendirme("ilk sayı söyleyin")
                veri1=self.ses_kayit()
                veri3=int(veri1)
                self.seslendirme("ikinci sayı söyleyin")
                veri2=self.ses_kayit()
                veri4=int(veri2)
                sonuc=veri3+veri4
                sonuc1=str(sonuc)
                self.seslendirme("işlemin sonucu  "+sonuc1)
                self.seslendirme("işlem tamam")
            elif "çıkarma" in veri:
                self.seslendirme("ilk sayı söyleyin")
                veri1=self.ses_kayit()
                veri3=int(veri1)
                self.seslendirme("ikinci sayı söyleyin")
                veri2=self.ses_kayit()
                veri4=int(veri2)
                sonuc=veri3-veri4
                sonuc1=str(sonuc)
                self.seslendirme("işlemin sonucu  "+sonuc1)
                self.seslendirme("işlem tamam")
            elif "bölme" in veri:
                self.seslendirme("ilk sayı söyleyin")
                veri1=self.ses_kayit()
                veri3=int(veri1)
                self.seslendirme("ikinci sayı söyleyin")
                veri2=self.ses_kayit()
                veri4=int(veri2)
                sonuc=veri3/veri4
                sonuc1=str(sonuc)
                self.seslendirme("işlemin sonucu  "+sonuc1)
                self.seslendirme("işlem tamam")
            elif "çarpma" in veri:
                self.seslendirme("ilk sayı söyleyin")
                veri1=self.ses_kayit()
                veri3=int(veri1)
                self.seslendirme("ikinci sayı söyleyin")
                veri2=self.ses_kayit()
                veri4=int(veri2)
                sonuc=veri3*veri4
                sonuc1=str(sonuc)
                self.seslendirme("işlemin sonucu  "+sonuc1)
                self.seslendirme("işlem tamam")
        elif "metin kaydı yap" in gelenses:
            self.seslendirme("dosyanın adı ne olsun")
            veri1=self.ses_kayit()
            dosya=open("{}.txt".format(veri1),"w")
            self.seslendirme("ne yazılmasını istiyorsun")
            veri2=self.ses_kayit()
            print(veri2,file=dosya)
            dosya.close()
            self.seslendirme("işlem tamamlandı")
        elif "oyunu aç" in gelenses:
            #oyunun gökyüzünü yaptığımız sınıf
            class Gokyuzu(Entity):
                def __init__(self):
                    super().__init__(
                        parent=scene,
                        model='sphere',
                        texture='sky_default',
                        double_sided=True,
                        scale=150,
                    )

            class Block(Button):
                def __init__(self, position=(0, 0, 0), texture='açıkcimen.jpg'):
                    super().__init__(
                        parent=scene,
                        position=position,
                        model='cube',
                        texture=texture,
                        color=color.color(0, 0, random.uniform(0.9, 1)),
                        origin_y=.5,

                    )

                chosenBlock = 1
                #blokları seçtiğimiz fonksiyon
                def update(self):
                    global chosenBlock

                    if held_keys['1']:
                        chosenBlock = 1
                        print("Beyaz küp seçildi")
                    if held_keys['2']:
                        chosenBlock = 2
                        print("Çimen seçildi")
                    if held_keys['3']:
                        chosenBlock = 3
                        print("Taş seçildi")
                    if held_keys['4']:
                        chosenBlock = 4
                        print("parke taşı")
                    if held_keys['5']:
                        chosenBlock = 5
                        print("odun")
                    if held_keys['6']:
                        chosenBlock = 6
                        print("yaprak")
                    if held_keys['7']:
                        chosenBlock = 7
                        print("cam blok seçildi")
                    if held_keys['8']:
                        chosenBlock = 8
                        print('kaya seçildi')
                #blokları kırıp koyduğumuz fonksiyon
                def input(self, key):
                    if self.hovered:
                        if key == 'right mouse down':
                            if chosenBlock == 1:
                                block = Block(position=self.position + mouse.normal, texture='white_cube')
                            elif chosenBlock == 2:
                                block = Block(position=self.position + mouse.normal, texture='grass')
                            elif chosenBlock == 3:
                                block = Block(position=self.position + mouse.normal, texture='brick')
                            elif chosenBlock == 4:
                                block = Block(position=self.position + mouse.normal, texture='tuğla.png')
                            elif chosenBlock == 5:
                                block = Block(position=self.position + mouse.normal, texture='odun.jpg')
                            elif chosenBlock == 6:
                                block = Block(position=self.position + mouse.normal, texture='yaprak.jpg')
                            elif chosenBlock == 7:
                                block = Block(position=self.position + mouse.normal, texture='cam.png')
                            elif chosenBlock == 8:
                                block = Block(position=self.position + mouse.normal, texture='kaya.png')

                        if key == 'left mouse down':
                            destroy(self)

            app = Ursina()

            player = FirstPersonController()
            gokyuzuz = Gokyuzu()
            #zemini oluşturduğumuz yer
            for x in range(25):
                for y in range(25):
                    block = Block(position=(x, 0, y))
                    block = Block(position=(x, -1, y), texture='toprak.png')
                    block = Block(position=(x, -2, y), texture='kaya.png')
            #ağacı tasarladığımız yer
            for q in range(1):
                for v in range(1):
                    block=Block(position=(q+16,1,v+14),texture='odun.jpg')
                    block = Block(position=(q + 16, 2, v + 14), texture='odun.jpg')
                    block = Block(position=(q + 16, 3, v + 14), texture='odun.jpg')
                    block = Block(position=(q + 16, 4, v + 14), texture='odun.jpg')
                    block = Block(position=(q + 16, 5, v + 14), texture='odun.jpg')
                    block = Block(position=(q + 16, 6, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 5, v + 13), texture='yaprak.jpg')
                    block = Block(position=(q + 15, 5, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 5, v + 15), texture='yaprak.jpg')
                    block = Block(position=(q + 17, 5, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 4, v + 13), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 4, v + 12), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 4, v + 15), texture='yaprak.jpg')
                    block = Block(position=(q + 16, 4, v + 16), texture='yaprak.jpg')
                    block = Block(position=(q + 14, 4, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 15, 4, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 17, 4, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 18, 4, v + 14), texture='yaprak.jpg')
                    block = Block(position=(q + 17, 4, v + 13), texture='yaprak.jpg')
                    block = Block(position=(q + 17, 4, v + 15), texture='yaprak.jpg')
                    block = Block(position=(q + 15, 4, v + 13), texture='yaprak.jpg')
                    block = Block(position=(q + 15, 4, v + 15), texture='yaprak.jpg')
            #tepeleri oluşturduğumuz yer
            for t in range(7):
                for u in range(7):
                    block = Block(position=(t + 18, 1, u + 18), texture='grass')
            for o in range(5):
                for i in range(5):
                    block = Block(position=(o + 20, 2, i + 20), texture='grass')
            for g in range(3):
                for h in range(3):
                    block = Block(position=(g + 22, 3, h + 22), texture='grass')
            for z in range(10):
                for j in range(10):
                    block = Block(position=(z+3, 1, j), texture='kaya.png')

            for a in range(8):
                for b in range(8):
                    block = Block(position=(a+3, 2, b), texture='kaya.png')
            for t in range(6):
                for e in range(6):
                    block = Block(position=(t+3, 3, e), texture='kaya.png')
            for r in range(4):
                for w in range(4):
                    block = Block(position=(r+3, 4, w), texture='kaya.png')
            for m in range(2):
                for n in range(2):
                    block = Block(position=(m+3, 5, n), texture='kaya.png')
            x=int(input("1'e bas ="))
            if x==1:
                self.seslendirme("oyun açılıyor")
                app.run()


        elif "terminal savaşını aç" in gelenses:
            self.seslendirme("terminalde oyun açılıyor")

            # karakterin ana classı(soyutlanmış)
            class Karakter(abc.ABC):
                @abc.abstractmethod
                def __init__(self, isim, unvan, saf, ozellik, guc, can):
                    self.__isim = isim
                    self.__unvan = unvan
                    self.__ozellik = ozellik
                    self.__guc = guc
                    self.__can = can
                    self.__saf = saf

                def tanitim(self):
                    print(
                        "=======================================================================================================")
                    time.sleep(0.3)
                    print(self.getisim(), self.getunvan(), "unvanıyla sahalarda! işte arenanın diz çüktüren",
                          self.getozellik(), "'ı")
                    time.sleep(0.3)
                    print(
                        "=======================================================================================================")

                def dusmantanitim(self):
                    time.sleep(0.6)
                    print(
                        "=======================================================================================================")
                    time.sleep(0.3)
                    print("KARŞISINDA İSE", self.getisim(), self.getunvan(), "adlı düşmaanımız var(", self.getozellik(),
                          ")")
                    time.sleep(0.3)
                    print(
                        "=======================================================================================================")

                def getisim(self):
                    return self.__isim

                def setisim(self, isim):
                    self.__isim = isim

                def getunvan(self):
                    return self.__unvan

                def setunvan(self, unvan):
                    self.__unvan = unvan

                def getsaf(self):
                    return self.__saf

                def setsaf(self, saf):
                    self.__saf = saf

                def getozellik(self):
                    return self.__ozellik

                def setozellik(self, ozellik):
                    self.__ozellik = ozellik

                def getguc(self):
                    return self.__guc

                def setguc(self, guc):
                    self.__guc = guc

                def getcan(self):
                    return self.__can

                def setcan(self, can):
                    self.__can = can

                def ozellikler(self):
                    print("=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_")
                    time.sleep(0.3)
                    print(self.getsaf(), " POWER => ", int(self.getguc()))
                    time.sleep(0.3)
                    print(self.getsaf(), " HEALT=> ", int(self.getcan()))
                    time.sleep(0.3)
                    print("=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_")

                # static method örnekleri
                @staticmethod
                def oyunhakkinda():
                    print("""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            bu oyun 3'er adet kahramanın ve düşmanın bulunduğu ve 1 er kişilik savaşın terminalde
            dönecek bir savaş oyunudur. oyuncu hareketlerini yani skillerini kendi seçecektir
            ve düşmanın seşeceği herhangi bir özellik (isim skill item vs...) bilgisayar tarafından
            verilecektir
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

                @staticmethod
                def itemskillfark():
                    print("""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            skilleri kendin seçebilirsin isteğine bağlı can ya da güç artımı yapabiliyorsun
            fakat item seçme hususu bilgisayara bırakılacaktır yani ne düşerse bahtına hesabı
            skillerde güç ve can artmaya meyillidir yani ne seçersen seç artış meydana gelecektir
            itemde ise can artışı da olabilir can azalışı da (mesela çaysa artar işkembe ise azalır gibi)
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

            # NİŞANCI SINIFI
            class Nisanciskill(Karakter):
                def __init__(self, isim, unvan, ozellik, saf, guc, can):
                    super().__init__(isim, unvan, ozellik, saf, guc, can)

                def geceninofkesi(self):
                    self.setguc(self.getguc() * 1.5)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE MADDİNG İN NİGHT")

                def anneduasi(self):
                    self.setcan(self.getcan() * 1.2)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı THE MOM'S PRAY")

                def seytaninmermileri(self):
                    self.setcan(self.getcan() * 1.3)
                    self.setguc(self.getguc() * 1.1)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı SATAN'S BULLETS")

                def ludeninferyadi(self):
                    self.setcan(self.getcan() * 1.1)
                    self.setguc(self.getguc() * 1.3)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı LUDE'S BELOW")

                def randomskill(self):
                    list = [self.anneduasi, self.seytaninmermileri, self.ludeninferyadi, self.geceninofkesi]
                    skill = random.choice(list)
                    skill()

                def skillsecimi(self):

                    secim = int(input("""
            NİŞANCI İÇİN hangi YETENEĞİ seçmek istiyorsun =
            ----------------------------------------------------------------------------- 
            GECENİN ÖFKESİ     =[1]     => gücü 1.5 oranında arttırır.               
            ANNE DUASI         =[2]     => canı 1.2 oranında arttırır.  
            ŞEYTANIN MERMİLERİ =[3]     => gücü ve canı 1.3 ve 1.1 oranlarında arttırır.
            LUDE'NİN FERYADI   =[4]     => gücü ve canı 1.1 ve 1.3 oranlarında arttırır.
            ----------------------------------------------------------------------------"""))
                    if secim == 1:
                        self.geceninofkesi()
                    elif secim == 2:
                        self.anneduasi()
                    elif secim == 3:
                        self.seytaninmermileri()
                    elif secim == 4:
                        self.ludeninferyadi()
                    else:
                        print("yanlış seçim. sıranız gitti")

            # BÜYÜCÜ SINIFI
            class BuyucuSkill(Karakter):
                def __init__(self, isim, unvan, ozellik, guc, saf, can):
                    super().__init__(isim, unvan, ozellik, guc, saf, can)

                def ruhsomuru(self):
                    self.setcan(self.getcan() * 1.4)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE SOUL FEED")

                def karanlikesaret(self):
                    self.setguc(self.getguc() * 1.15)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE DARK BRAVE")

                def karakalkan(self):
                    self.setcan(self.getcan() * 1.2)
                    self.setguc(self.getguc() * 1.2)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE DARK SHIELD")

                def padisahinDuasi(self):
                    self.setcan(self.getcan() * 1.3)
                    self.setguc(self.getguc() * 1.1)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE KİNG'S PRAY")

                def randomskill(self):
                    list = [self.ruhsomuru, self.karanlikesaret, self.karakalkan, self.padisahinDuasi]
                    skill = random.choice(list)
                    skill()

                def skillsecimi(self):

                    secim = int(input("""           
            BÜYÜCÜ İÇİN hangi skilli seçmek istiyorsun
            ////////////////////////////////////////////////////////////////////////
            RUH SÖÜRÜSÜ         =[1]            => canı 1.4  oranında arttırır
            KARANLIK CESARETİ   =[2]            => gücü 1.15 oranında arttırır.
            KARAKALKAN          =[3]            => güç ve canı arttırır.
            PADİŞAH'IN DUASI    =[4]            => güç ve canı arttırır.
            ////////////////////////////////////////////////////////////////////////"""))
                    if secim == 1:
                        self.ruhsomuru()
                    elif secim == 2:
                        self.karanlikesaret()
                    elif secim == 3:
                        self.karakalkan()
                    elif secim == 4:
                        self.padisahinDuasi()
                    else:
                        # bunu sesli yazdır
                        print("yanlış seçim. sıranız gitti")

            # TANK SINIFI
            class TankSkill(Karakter):
                def __init__(self, isim, unvan, ozellik, saf, guc, can):
                    super().__init__(isim, unvan, ozellik, saf, guc, can)

                def metanet(self):
                    self.setcan(self.getcan() * 1.3)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :METANET")

                def amansizhucum(self):
                    self.setguc(self.getguc() * 1.5)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :AMANSIZ HÜCUM")

                def cesaret(self):
                    self.setcan(self.getcan() * 1.3)
                    self.setguc(self.getguc() * 1.1)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE BRAVE ATTACK")

                def milletinduasi(self):
                    self.setguc(self.getguc() * 1.8)
                    self.setcan(self.getcan() * 0.8)
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>", self.getsaf(), "bunu kullandı :THE CİTİZEN'S PRAY")

                def randomskill(self):
                    list = [self.metanet, self.amansizhucum, self.milletinduasi, self.cesaret]
                    skill = random.choice(list)
                    skill()

                def skillsecimi(self):

                    secim = int(input("""       
            TANK için hangi skilli seçmek istiyorsun
            ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            METANET         =[1]            =>      Canı 1.3 oranında arttırır.
            AMANSIZ HÜCUM   =[2]            =>      Gücü 1.5 oranında arttırır.
            CESARET         =[3]            =>      canı canı 1.3 gücü 1.1 oranında arttırır.
            MİLLET'İN DUASI =[4]            =>      canı 1.8 oranında arttırır fakat gücün düşer.
            ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  """))
                    if secim == 1:
                        self.metanet()
                    elif secim == 2:
                        self.amansizhucum()
                    elif secim == 3:
                        self.cesaret()
                    elif secim == 4:
                        self.milletinduasi()
                    else:
                        print("yanlış seçim. sıranız gitti")

            # İTEMLER ANA BAŞLIĞINDA:
            class Items(abc.ABC):
                @abc.abstractmethod
                def __init__(self, canartis, gucartis):
                    self.__canartis = canartis
                    self.__gucartis = gucartis

                def getcanartis(self):
                    return self.__canartis

                def setcanartis(self, canartis):
                    self.__canartis = canartis

                def getgucartis(self):
                    return self.__gucartis

                def setgucartis(self, gucartis):
                    self.__gucartis = gucartis

            class Buyucuitems(Items):
                def __init__(self, canartis, gucartis):
                    super().__init__(canartis, gucartis)

                def kahve(self):
                    a = self.getcanartis() + 2
                    self.setcanartis(a)
                    print("büyücünün şansına kahve geldi! bu sayede ona 2 birim can gelecek")

                def zehir(self):
                    a = self.getgucartis() - 2
                    self.setgucartis(a)
                    print("büyücünün şansına zehir geldi! bu yüzden ondan 2 birim güç düşecek")

                def frappe(self):
                    a = self.getgucartis() + 2
                    self.setgucartis(a)
                    print("büyücünün şansına frappe geldi! bu sayede ona 2 birim güç gelecek")

                def bozukyogurt(self):
                    a = self.getgucartis() - 2
                    self.setgucartis(a)
                    print("büyücünün şansına bozuk yoğurt geldi! bu yüzden ondan 2 birim güç azalacak")

                def randomitemat(self):
                    list = [self.kahve, self.zehir, self.frappe, self.bozukyogurt]
                    aytım = random.choice(list)
                    aytım()

            class Nisanciitems(Items):
                def __init__(self, canartis, gucartis):
                    super().__init__(canartis, gucartis)

                def Icetea(self):
                    a = self.getgucartis() + 1
                    self.setgucartis(a)
                    print("nişancının şansına Ice Tea geldi! bu sayede gücünde +1 artış olacak")

                def bozukyogurt(self):
                    a = self.getgucartis() - 1
                    self.setgucartis(a)
                    print("nişancının şansına BOZUK YOĞURT geldi! bu yüzden gücünde -1 azalma olacak")

                def grapejuice(self):
                    a = self.getcanartis() + 1
                    self.setcanartis(a)
                    print("nişancının şansına ÜZÜM SUYU geldi! bu sayede canında +1 artış olacak")

                def sushi(self):
                    a = self.getcanartis() - 1
                    self.setcanartis(a)
                    print("nişancımız yanlışlıkla SUŞİ yedi! bu yüzden canında -1 azalma olacak")

                def randomitemat(self):
                    list = [self.Icetea, self.bozukyogurt, self.grapejuice, self.sushi]
                    aytım = random.choice(list)
                    aytım()

            class Tankitems(Items):
                def __init__(self, canartis, gucartis):
                    super().__init__(canartis, gucartis)

                def cola(self):
                    a = self.getcanartis() + 2
                    self.setcanartis(a)
                    print("tankın şansına COLA geldi! bu sayede ona 2 birim can gelecek")

                def sirke(self):
                    a = self.getcanartis() + 2
                    self.setcanartis(a)
                    print("tankın şansına sirke geldi! bu yüzden ondan 2 birim can gidecek")

                def sprite(self):
                    a = self.getgucartis() + 2
                    self.setcanartis(a)
                    print("tankın şansına sprite geldi! bu sayede ona 2 birim güç gelecek")

                def scheweppews(self):
                    a = self.getgucartis() + 2
                    self.setcanartis(a)
                    print("tankın şansına scheweppes geldi! bu sayede ondan 2 birim güç gidecek")

                def randomitemat(self):
                    list = [self.cola, self.sirke, self.sprite, self.scheweppews]
                    aytım = random.choice(list)
                    aytım()

            # karakterlerin yetenek nesnesi:
            nisanci = Nisanciskill("iskender", "toskoparan", "kahraman", "nisanci", 15, 150)
            dnisanci = Nisanciskill("Timur", "Emir", "düşman", "nisanci", 15, 150)
            buyucu = BuyucuSkill("urban", "macar", "kahraman", "büyücü", 20, 150)
            dbuyucu = BuyucuSkill("Voyvoda", "kazıklı", "düşman", "büyücü", 20, 150)
            tank = TankSkill("IV. Murat", "hükümdar", "kahraman", "tank", 10, 200)
            dtank = TankSkill("Ahmet pasha", "Kavalalı", "düşman", "tank", 10, 200)
            # karakterlerin itemi
            nitem = Nisanciitems(0, 0)
            bitem = Buyucuitems(0, 0)
            titem = Tankitems(0, 0)

            nisanci.oyunhakkinda()
            nisanci.itemskillfark()
            # polimorpishm örneği
            print("KAHRAMANLARIMIZ: ")
            liste = [nisanci, buyucu, tank]
            for i in range(len(liste)):
                print(liste[i].getisim())
            print("DÜŞMANLARIMIZ: ")
            dliste = [dnisanci, dbuyucu, dtank]
            for i in range(len(dliste)):
                print(liste[i].getisim())
            # FIGHT DÖNECEK YER

            c = 2
            scm = 2

            list = [nisanci, buyucu, tank]  # kahramanlarımızın olduğu liste var (EL İLE SEÇİM)
            ilist = [nitem, bitem, titem]  # kahramanlarımızın olduğu liste

            dlist = [dnisanci, dbuyucu, dtank]  # düşmanlarımızın olduğu liste (RANDOM SEÇİM)
            dusman = random.choice(dlist)
            if dusman == dnisanci:
                scm = nitem
            if dusman == dbuyucu:
                scm = bitem
            if dusman == dtank:
                scm = titem
            q = 1
            syyc = 0
            while q == 1:
                a = int(input("""
                -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                KAHRAMANINI SEÇ
                NİŞANCI İÇİN ((1))
                BÜYÜCÜ İÇİN  ((2))
                TANK İÇİN    ((3)) 
                -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ =>"""))
                if (a == 1) or (a == 2) or (a == 3):
                    q = 2
                else:
                    syyc += 1
                    print("seçimi yanlış yaptınız tekrar deneyiniz")
                    if syyc % 4 == 0:
                        print("LÜTFEN 1 ya da 2 ya da 3'ü seçin artık!")

            a = a - 1
            sayac = 0
            time.sleep(1)
            list[a].tanitim()
            time.sleep(1)
            dusman.dusmantanitim()
            time.sleep(1)
            ccc = 1
            while ccc <= 1:
                list[a].ozellikler()
                time.sleep(0.5)
                dusman.ozellikler()
                time.sleep(1)
                list[a].skillsecimi()  # bizim karakterim skilli el ile seçildi
                time.sleep(1)
                dusman.randomskill()  # düşman karakterin random skill seçildi
                time.sleep(1)
                list[a].setcan(list[a].getcan() + ilist[a].getcanartis())
                list[a].setguc(list[a].getguc() + ilist[a].getgucartis())
                time.sleep(1)

                dusman.setcan(dusman.getcan() + scm.getcanartis())
                dusman.setguc(dusman.getguc() + scm.getgucartis())
                sayac += 1
                if sayac % 3 == 0:
                    scm.randomitemat()
                    ilist[a].randomitemat()
                    list[a].setcan(list[a].getcan() + ilist[a].getcanartis())

                list[a].setcan(list[a].getcan() - dusman.getguc())
                dusman.setcan(dusman.getcan() - list[a].getguc())
                if int(list[a].getcan()) <= 0:
                    list[a].setcan(0)
                if int(dusman.getcan()) <= 0:
                    dusman.setcan(0)

                if (list[a].getcan() < 1):
                    list[a].ozellikler()
                    time.sleep(0.5)
                    dusman.ozellikler()
                    print(dusman.getisim(), "kazandı")
                    ccc = 2

                elif (dusman.getcan() < 1):
                    list[a].ozellikler()
                    time.sleep(0.5)
                    dusman.ozellikler()
                    print(list[a].getisim(), " kazandı")
                    ccc = 2



    def test(self,voice):
        if "hey piton" in voice or "piton" in voice:
            asistan.seslendirme("efendim ")
            voice = asistan.ses_kayit()
            if voice!="":
                ses=voice.lower()
                print(voice.capitalize())
                asistan.ses_karsilik(ses)

asistan=Sesliasistan()

while True:
     ses=asistan.ses_kayit()
     if (ses!=""):
         ses=ses.lower()
         print(ses)
         asistan.test(ses)




