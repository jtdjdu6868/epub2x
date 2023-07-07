import os
import shutil
import zipfile
import json
import base64

GPUID = 0
MODEL = 'RealESRGAN-anime'
SCALE = 2
NOISE = -1
TARGET_SCALE = 2

SRC_PATH = 'sources'
DEST_PATH = 'output'
TMP_PATH = 'tmp'

def decompress(src_filename, src_path, dest_path):
    epub_path = os.path.join(src_path, src_filename)
    epub_name = os.path.splitext(src_filename)[0]
    epub_dir = os.path.join(dest_path, epub_name)
    os.makedirs(epub_dir, exist_ok=True)

    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        zip_ref.extractall(epub_dir)
    return epub_dir


if __name__ == '__main__':
    epub_list = [f for f in os.listdir(SRC_PATH) if (os.path.isfile(os.path.join(SRC_PATH, f)) and f.endswith('.epub'))]
    for epub in epub_list:
        # decompress
        epub_dir = decompress(epub, SRC_PATH, TMP_PATH)

        # 2x it
        img_path = os.path.join(epub_dir, 'EPUB', 'images')
        img_list = [os.path.join(img_path, f) for f in os.listdir(img_path)]
        json_data = {
            'gpuid': GPUID,
            'inputpath': img_list,
            'model': MODEL,
            'modelscale': SCALE,
            'modelnoise': NOISE,
            'outputpath': img_path,
            'targetscale': TARGET_SCALE,
            'tta': False
        }
        json_str = json.dumps(json_data)
        json_base64 = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

        os.system(f'final2x-core -b {json_base64}')

        # delete all orig img_list
        for img in img_list:
            os.remove(img)
        
        # copy output to original dir
        output_dir = os.path.join(img_path, 'outputs')
        output_list = [f for f in os.listdir(output_dir)]
        for output in output_list:
            os.rename(os.path.join(output_dir, output), os.path.join(img_path, output.split('-', 1)[1]))
        os.rmdir(output_dir)