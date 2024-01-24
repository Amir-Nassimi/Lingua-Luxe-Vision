from SDK.Generation_SDK import TextToImage as SDK_generation
# from Keras.Generation_Keras import TextToImage as Keras_generation
from Diffusion.Generation_StableDiff import TextToImage as StableDiff_generation


class ImageGeneration:
    def __init__(self,
                 method,
                 model='stable-diffusion-v1-5',
                 activation_key='sk-7kNckYYDo8QDgS2P4iJ4YvRxRTWqsxyb6kGDGNr0wi6k6AQd',
                 image_size=512,
                 to_cuda=False,
                 guidance_scale=5,
                 seed=31):

        if method == 'Detailed':
            self.my_class = [StableDiff_generation(model=model, image_size=image_size, to_cuda=to_cuda, guidance_scale=guidance_scale, seed=seed)]
        elif method == 'Simple':
            self.my_class = [SDK_generation(activation_key=activation_key, image_size=image_size)]
        elif method == 'Both':
            self.my_class = [StableDiff_generation(model=model, image_size=image_size, to_cuda=to_cuda,
                                                   guidance_scale=guidance_scale, seed=seed),
                             SDK_generation(activation_key=activation_key, image_size=image_size)]
        else:
            raise ValueError(f"The method [{method}] is not defined!")

    def generate_images(self, text):
        images = []

        for method in self.my_class:
            images.append(method.generation(text))

        return images