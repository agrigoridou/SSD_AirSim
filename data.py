import airsim
import numpy as np
import cv2
import os
import time

# Σύνδεση με AirSim
client = airsim.CarClient()
client.confirmConnection()

# Ορισμός φακέλου για το σενάριο
scenario = "backlight"   
output_folder = f"dataset/{scenario}"
os.makedirs(output_folder, exist_ok=True)

# Αριθμός εικόνων που θες να αποθηκεύσεις
n_images = 200

for i in range(n_images):
    response = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
    ])[0]

    if response.width == 0:
        continue

    # Μετατροπή σε RGB
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # Αποθήκευση με timestamp
    timestamp = time.strftime("%H%M%S")
    filename = os.path.join(output_folder, f"{scenario}_{i}_{timestamp}.jpg")
    cv2.imwrite(filename, img_rgb)

    print(f"[OK] Αποθηκεύτηκε: {filename}")
    time.sleep(0.2)  # μικρή παύση για να μην τραβάει όλα τα frames μαζί

print("[FINISHED] Συλλογή εικόνων ολοκληρώθηκε.")
