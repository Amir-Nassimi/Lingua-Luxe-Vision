import os
import sys
import shlex
import torch
from diffusers import AutoPipelineForText2Image
from googletrans import Translator


class TextToImage:
    def __init__(self, model, image_size, to_cuda, guidance_scale=5, seed=31):
        self.translator = Translator(service_urls=['translate.google.com', 'translate.google.co.kr'])

        self.to_cuda = to_cuda
        self.image_size = image_size
        self.guidance_scale = guidance_scale
        self.seed = seed

        if not to_cuda:
            commandline_args = os.environ.get('COMMANDLINE_ARGS', "")
            commandline_args = os.environ.get('COMMANDLINE_ARGS', "--skip-torch-cuda-test --no-half")
            sys.argv += shlex.split(commandline_args)

            self.pipeline = AutoPipelineForText2Image.from_pretrained("runwayml/" + model, torch_dtype=torch.float32, variant="fp16")

        else:
            self.pipeline = AutoPipelineForText2Image.from_pretrained("runwayml/" + model, torch_dtype=torch.float32, variant="fp16").to("cuda")
            self.generator = torch.Generator("cuda").manual_seed(self.seed)


    def generation(self, text):
        translated = self.translator.translate(text, dest='en', src='fa').text
        if not self.to_cuda:
            image = self.pipeline(translated, height=self.image_size, width=self.image_size, guidance_scale=self.guidance_scale).images[0]
        else:
            image = self.pipeline(translated, height=self.image_size, width=self.image_size, guidance_scale=self.guidance_scale, generator=self.generator).images[0]

        return image