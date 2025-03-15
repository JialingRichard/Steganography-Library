import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

class DCTSteganography:
    def embed(self, cover_image_path, secret_image_path, stego_image_path, block_size=8):
        cover_img = Image.open(cover_image_path).convert("RGB")
        secret_img = Image.open(secret_image_path).convert("RGB")
        cover_data = np.array(cover_img)
        secret_data = np.array(secret_img)
        secret_height, secret_width, _ = secret_data.shape
        cover_height, cover_width, _ = cover_data.shape
        if secret_height > cover_height or secret_width > cover_width:
            raise ValueError("Secret image too large for cover image")
        stego_data = cover_data.copy()
        for i in range(0, secret_height, block_size):
            for j in range(0, secret_width, block_size):
                for channel in range(3):
                    block = cover_data[i:i + block_size, j:j + block_size, channel]
                    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                    secret_pixel = secret_data[i // block_size, j // block_size, channel] if i < secret_height and j < secret_width else 0
                    dct_block[0, 0] = (dct_block[0, 0] & ~1) | (secret_pixel & 1)
                    stego_data[i:i + block_size, j:j + block_size, channel] = np.round(idct(idct(dct_block.T, norm='ortho').T, norm='ortho'))
        Image.fromarray(stego_data.astype(np.uint8)).save(stego_image_path)

    def extract(self, stego_image_path, secret_width, secret_height, extracted_image_path, block_size=8):
        stego_img = Image.open(stego_image_path).convert("RGB")
        stego_data = np.array(stego_img)
        extracted_data = np.zeros((secret_height, secret_width, 3), dtype=np.uint8)
        for i in range(0, secret_height, block_size):
            for j in range(0, secret_width, block_size):
                for channel in range(3):
                    block = stego_data[i:i + block_size, j:j + block_size, channel]
                    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                    extracted_data[i // block_size, j // block_size, channel] = (dct_block[0, 0] & 1) * 255
        Image.fromarray(extracted_data.astype(np.uint8)).save(extracted_image_path)