import qrcode

# 创建 QR 码对象，设置 H 级纠错
qr = qrcode.QRCode(
    version=12,  # 控制二维码尺寸（1-40），越大可存储更多数据
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 最高级别 H（可恢复30%数据）
    box_size=20,  # 每个点的大小
    border=10      # 边框大小
)

# 添加数据
data = "Hello, Steganography!"
qr.add_data(data)
qr.make(fit=True)

# 生成二维码图像
img = qr.make_image(fill="black", back_color="white")
img.show()  # 显示二维码
img.save("./dataset/qrcode_h.png")  # 保存二维码


# import pyqrcode

# # 数据
# data = "This is a QR code with high error correction and customization"

# # 创建 QR 码对象，设置不同的参数
# qr = pyqrcode.create(
#     data,
#     error='H',              # 错误修正级别（H 最高）
#     version=10,             # 版本，10 代表较大的二维码
#     module_color='black',    # 模块颜色为蓝色
#     background='white',    # 背景颜色为白色
# )

# # 保存 QR 码为 PNG 图片
# qr.png('./dataset/qrcode_h.png', scale=10, quiet_zone=5, box_size=8)
