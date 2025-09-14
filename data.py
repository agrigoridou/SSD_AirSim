import airsim, cv2, numpy as np

client = airsim.CarClient()
client.confirmConnection()

for i in range(200):
    response = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
    ])[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)  
    img_rgb = img1d.reshape(response.height, response.width, 3)
    cv2.imwrite(f"dataset/image_{i}.png", img_rgb)
