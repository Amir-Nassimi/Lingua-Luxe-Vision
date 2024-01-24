import os
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from googletrans import Translator


class TextToImage:
    def __init__(self, activation_key, image_size):
        os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
        os.environ['STABILITY_KEY'] = activation_key

        self.translator = Translator(service_urls=['translate.google.com', 'translate.google.co.kr'])
        self.stability_api = client.StabilityInference(key=os.environ['STABILITY_KEY'],
                                                       verbose=True,
                                                       engine="stable-diffusion-xl-1024-v1-0")
        self.image_size = image_size

    def generation(self, text):
        translated = self.translator.translate(text, dest='en', src='fa')
        answers = self.stability_api.generate(prompt=translated.text,
                                              seed=4253978046,
                                              steps=50,
                                              cfg_scale=8.0,
                                              width=self.image_size,
                                              height=self.image_size,
                                              samples=1,
                                              sampler=generation.SAMPLER_K_DPMPP_2M)

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    return None
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary)).convert('RGB')
                    return img
