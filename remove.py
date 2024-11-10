from rembg import remove
from PIL import Image
import os
input_folder_path = 'D:\guide_pic - Copy'
output_folder_path = f'{input_folder_path}_rmbg'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
for root, dirs, files in os.walk(input_folder_path):
    for file in files:
        filename, extension = os.path.splitext(file)
        if extension == '.jpg':
            input = Image.open(f'{input_folder_path}/{filename}.jpg')
            output = remove(input)
            output.save(f'{output_folder_path}/{filename}.png')