import argparse

from Models.Image_Generation import ImageGeneration


class Execution:
    def __init__(self, **kwargs):
        self.model = self.get_model(kwargs.get('model'))
        self.input = kwargs.get('text')
        self.output = kwargs.get('output')

    @staticmethod
    def get_model(model_detail):
        return ImageGeneration(model_detail)
    
    def save_imgs(self, img, id):
        img.save(f'{self.output}/{id+1}.jpg')
        
    def run(self):
        imgs = self.model.generate_images(self.input)
        for indx, img in enumerate(imgs):
            self.save_imgs(img, indx)


def main():
    parser = argparse.ArgumentParser(description="Lingua Luxe Vision")
    
    parser.add_argument('--model', required=False, type=str, default='Simple', help='Type of the model; either "Detailed", "Simple" or "Both"')
    parser.add_argument('--text', required=True, type=str, help='Input text - in Persian language')
    parser.add_argument('--output', required=True, type=str, help='Output directory')
    
    args = parser.parse_args()

    executer = Execution(**vars(args))
    executer.run()

if __name__ == "__main__":
    main()