import keras_cv
from googletrans import Translator


class TextToImage:
    def __init__(self, image_size):
        self.translator = Translator(service_urls=['translate.google.com', 'translate.google.co.kr'])
        self.model = keras_cv.models.StableDiffusion(img_width=image_size, img_height=image_size, jit_compile=False)

    def generation(self, text, repeat):
        translated = self.translator.translate(text, dest='en', src='fa')
        images = self.model.text_to_image(translated.text, batch_size=repeat)
        return images
