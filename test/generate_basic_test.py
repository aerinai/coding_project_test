from unittest import TestCase
from PIL import Image, ImageDraw, ImageFont
import textwrap

config = '/templates/config.csv'


class GenerateTiffs(TestCase):
    def test_generate_lorem_ipsum(self):
        config = self.read_config()
        for item in config:
            lorem_ipsum = self.get_text('./templates/loremipsum.txt')
            lorem_ipsum = lorem_ipsum.replace('{FULL_NAME}', item.get('FULL_NAME', 'Nully McNullerson'))
            lorem_ipsum = lorem_ipsum.replace('{ADDRESS}', item.get('ADDRESS', '123 Null Ln'))
            lorem_ipsum = lorem_ipsum.replace('{CITY}', item.get('CITY', 'Nullville'))
            lorem_ipsum = lorem_ipsum.replace('{STATE}', item.get('STATE', 'MO'))
            lorem_ipsum = lorem_ipsum.replace('{ZIP}', item.get('ZIP', '12345'))

            name = item.get('FULL_NAME', 'John Smith')
            # replace spaces of name with underscore
            name = name.replace(' ', '_')
            self.create_image(lorem_ipsum, f'lorem_ipsum_{name}')

    def create_image(self, text, file_name):
        # Create a new image with white background
        img = Image.new('RGB', (850, 1100), color=(255, 255, 255))

        # Initialize the drawing context with
        draw = ImageDraw.Draw(img)

        # Create font object with the font file and specify
        # desired size (You may need to adjust the size and the path to the font file)
        font = ImageFont.truetype('cour.ttf', size=16)

        # Wrap the text
        text_new = ''
        for txt in text.split('\n'):
            print(f'Current Text_new: {text_new}')
            wrapper = textwrap.TextWrapper(width=80)  # Adjust as necessary
            word_list = wrapper.wrap(text=txt)
            if len(word_list) == 0:
                text_new += '\n'
                continue
            print(f'Word List: {word_list}')
            for ii in word_list[:-1]:
                text_new += ii + '\n'
            text_new += word_list[-1]
            text_new += '\n'

        # Starting position of the message
        (x, y) = (50, 25)

        color = 'rgb(0, 0, 0)'  # black color

        # Draw the text on the background
        draw.text((x, y), text_new, fill=color, font=font)

        # Save the image in tif file
        img.save(f'./generated_files/{file_name}.tiff', compression='tiff_lzw')

    def read_config(self):
        result = []
        # Read config.csv and parse each line
        csv = open(config, 'r')
        lines = csv.readlines()
        for line in lines:
            data = line.split(',')
            result.append({
                'FULL_NAME': data[0],
                'ADDRESS': data[1],
                'CITY': data[2],
                'STATE': data[3],
                'ZIP': data[4]
            })
        csv.close()
        return result

    def get_text(self, path):
        with open(path, 'r') as file:
            return file.read()
