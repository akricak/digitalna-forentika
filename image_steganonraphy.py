# This is a sample Python script.
import numpy as np
import cv2

class DCTStego:
    def __init__(self):
        pass

    def dct_transform(self, image):
        channels = []
        for channel in cv2.split(image):
            channels.append(cv2.dct(np.float32(channel)))
        return cv2.merge(channels)

    def idct_transform(self, image_dct):
        channels = []
        for channel in cv2.split(image_dct):
            channels.append(cv2.idct(channel))
        return cv2.merge(channels)

    def reduce_noise(self, image, sigma=1.5):
        # Konvertujte sliku u odgovarajući tip
        image = np.uint8(image)
        # Smanjivanje šuma u slici pomoću Gausovog filtra
        return cv2.fastNlMeansDenoisingColored(image, None, sigma, sigma, 7, 21)

    def reduce_noise1(self, image, sigma=1.5):
        image = np.clip(image, 0, 255)
        # Konvertujte sliku u odgovarajući tip
        image = np.uint8(image)
        # Smanjivanje šuma u slici pomoću Gausovog filtra
        return cv2.fastNlMeansDenoisingColored(image, None, sigma, sigma, 3, 16)

    def encode_image(self):
        cover_image_path = input("Unesite putanju do pokrivne slike: ")
        secret_image_path = input("Unesite putanju do tajne slike: ")

        cover_image = cv2.imread(cover_image_path)
        if cover_image is None:
            print("Greška: Nije moguće učitati pokrivnu sliku.")
            return None

        secret_image = cv2.imread(secret_image_path)
        if secret_image is None:
            print("Greška: Nije moguće učitati tajnu sliku.")
            return None

        if cover_image.shape[0] != secret_image.shape[0] or cover_image.shape[1] != secret_image.shape[1]:
            print("Greška: Dimenzije tajne slike se ne podudaraju sa dimenzijama pokrivne slike.")
            return None

        cover_dct = self.dct_transform(cover_image)
        secret_dct = self.dct_transform(secret_image)

        alpha = 0.001

        stego_dct = cover_dct + alpha * secret_dct

        stego_image = self.idct_transform(stego_dct)

        stego_image = self.reduce_noise(stego_image)  # Smanjivanje šuma
        cv2.imshow("Stego slika", stego_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        stego_image_path = input("Unesite putanju za čuvanje rezultujuće stego slike: ")
        if stego_image_path:
            cv2.imwrite(stego_image_path, stego_image)

        return stego_image

    def decode_image(self):
        stego_image_path = input("Unesite putanju do stego slike: ")

        stego_image = cv2.imread(stego_image_path)
        if stego_image is None:
            print("Greška: Nije moguće učitati stego sliku.")
            return None

        alpha = 0.1
        secret_dct = (stego_image - alpha * self.dct_transform(stego_image)) / alpha
        secret_image = self.idct_transform(secret_dct)
        secret_image = self.reduce_noise1(secret_image)  # Smanjivanje šuma

        cv2.imshow("Tajna slika", secret_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        secret_image_path = input("Unesite putanju za čuvanje rezultujuće tajne slike: ")
        if secret_image_path:
            cv2.imwrite(secret_image_path, secret_image)

        return secret_image


dct_stego = DCTStego()
stego_image = dct_stego.encode_image()
#secret_image = dct_stego.decode_image()




























































































































































































































































