import cv2
import numpy as np

def add_gaussian_noise(image: np.ndarray, mean=0, sigma=25) -> np.ndarray:
    """
    向图像中添加高斯噪声。
    :param image: 输入图像（numpy数组）
    :param mean: 高斯噪声的均值
    :param sigma: 高斯噪声的标准差
    :return: 添加噪声后的图像
    """
    # 生成高斯噪声
    gaussian_noise = np.random.normal(mean, sigma, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, gaussian_noise)  # 将噪声添加到图像中
    return noisy_image