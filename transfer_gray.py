import cv2

# 读取图像并转换为灰度图
def convert_to_grayscale(image_path, output_path):
    # 读取原始图像
    image = cv2.imread(image_path)
    
    # 转换为灰度图
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 保存灰度图
    cv2.imwrite(output_path, grayscale_image)
    print(f"Grayscale image saved as {output_path}")

# 示例用法
convert_to_grayscale('./dataset/cover.jpg', './dataset/cover_gray.jpg')
