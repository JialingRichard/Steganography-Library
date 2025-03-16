from PIL import Image

class LSBSteganography:
    def __init__(self, bits_to_hide=1):
        self.bits_to_hide = bits_to_hide

    def encode(self, cover_path, secret_path, stego_path):
        """
        在载体图像中隐藏秘密图像，使用多个最低有效位。

        参数：
            cover_path (str): 载体图像的路径。
            secret_path (str): 秘密图像的路径。
            stego_path (str): 输出图像的路径。
        """
        cover_image = Image.open(cover_path).convert('RGB')
        secret_image = Image.open(secret_path).convert('RGB')

        cover_width, cover_height = cover_image.size
        secret_width, secret_height = secret_image.size

        # 检查载体图像是否足够大以隐藏秘密图像
        if secret_width > cover_width or secret_height > cover_height:
            raise ValueError("载体图像太小，无法隐藏秘密图像。")

        cover_pixels = cover_image.load()
        secret_pixels = secret_image.load()

        # 掩码，用于保留最低有效位
        mask = (1 << self.bits_to_hide) - 1  # 生成掩码

        for x in range(secret_width):
            for y in range(secret_height):
                # 获取秘密图像的 RGB 值
                secret_r, secret_g, secret_b = secret_pixels[x, y]

                # 获取载体图像的 RGB 值
                cover_r, cover_g, cover_b = cover_pixels[x, y]

                # 将秘密图像的高位替换载体图像的低位
                cover_r = (cover_r & ~(mask)) | ((secret_r >> (8 - self.bits_to_hide)) & mask)
                cover_g = (cover_g & ~(mask)) | ((secret_g >> (8 - self.bits_to_hide)) & mask)
                cover_b = (cover_b & ~(mask)) | ((secret_b >> (8 - self.bits_to_hide)) & mask)

                # 更新载体图像的像素值
                cover_pixels[x, y] = (cover_r, cover_g, cover_b)

        # noise
        import numpy as np
        import cv2

        # noise
        np_cover_image = np.array(cover_image) # 将 PIL Image 对象转换为 numpy 数组
        shape = np_cover_image.shape
        gaussian_noise = np.random.normal(0, 3, shape).astype(np.uint8)
        noisy_image = cv2.add(np_cover_image, gaussian_noise) # 使用 numpy 数组

        # 保存隐藏了秘密图像的载体图像
        Image.fromarray(noisy_image).save(stego_path) # 将 numpy 数组转换为 PIL Image 对象并保存


        # 保存隐藏了秘密图像的载体图像
        # cover_image.save(stego_path)

    def decode(self, stego_path, extracted_path, secret_width, secret_height):
        """
        从隐藏图像中提取秘密图像，使用多个最低有效位。

        参数：
            stego_path (str): 隐藏图像的路径。
            extracted_path (str): 输出秘密图像的路径。
            secret_width (int): 秘密图像的宽度。
            secret_height (int): 秘密图像的高度。
        """
        stego_image = Image.open(stego_path).convert('RGB')
        stego_pixels = stego_image.load()

        secret_image = Image.new('RGB', (secret_width, secret_height))
        secret_pixels = secret_image.load()

        # 掩码，用于提取最低有效位
        mask = (1 << self.bits_to_hide) - 1  # 生成掩码

        for x in range(secret_width):
            for y in range(secret_height):
                # 获取隐藏图像的 RGB 值
                stego_r, stego_g, stego_b = stego_pixels[x, y]

                # 从隐藏图像的最低有效位提取秘密图像的 RGB 值
                secret_r = (stego_r & mask) << (8 - self.bits_to_hide)
                secret_g = (stego_g & mask) << (8 - self.bits_to_hide)
                secret_b = (stego_b & mask) << (8 - self.bits_to_hide)

                # 设置秘密图像的像素值
                secret_pixels[x, y] = (secret_r, secret_g, secret_b)

        # 保存提取的秘密图像
        secret_image.save(extracted_path)