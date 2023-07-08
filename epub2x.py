import os
import shutil
import zipfile
from FCA.Adapter import Adapter

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
    final2x_config = {
        'gpuid': GPUID,
        'model': MODEL,
        'modelscale': SCALE,
        'modelnoise': NOISE,
        'targetscale': TARGET_SCALE,
        'tta': False
    }
    adapter = Adapter(final2x_config)
    
    if os.path.exists(TMP_PATH):
        shutil.rmtree(TMP_PATH)
    epub_list = [f for f in os.listdir(SRC_PATH) if (os.path.isfile(os.path.join(SRC_PATH, f)) and f.endswith('.epub'))]
    for epub in epub_list:
        # decompress
        epub_dir = decompress(epub, SRC_PATH, TMP_PATH)

        # 2x it
        # walk through all folder called 'images' under epub_dir
        for root, dirs, files in os.walk(epub_dir):
            if os.path.basename(root) == 'images':
                print(f'Found images folder: {root}')
                for src_img in files:
                    src_img_path = os.path.join(root, src_img)
                    print(src_img_path)
                    adapter.queue(src_img_path, src_img_path)
            


        # compress
        os.makedirs(DEST_PATH, exist_ok=True)
        shutil.make_archive(os.path.join(DEST_PATH, epub), 'zip', epub_dir)
        if os.path.exists(os.path.join(DEST_PATH, epub)):
            os.remove(os.path.join(DEST_PATH, epub))
        os.rename(os.path.join(DEST_PATH, epub + '.zip'), os.path.join(DEST_PATH, epub))