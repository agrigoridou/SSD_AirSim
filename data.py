import airsim
import numpy as np
import cv2
import os
import time

# Σύνδεση με AirSim
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# Ορισμός φακέλου για το dataset
scenario = "scenario_drive3"
output_folder = f"dataset/{scenario}"
os.makedirs(output_folder, exist_ok=True)

# Ρυθμίσεις οδήγησης
car_controls.throttle = 1.0   # ταχύτητα (0.0 - 1.0)
car_controls.steering = 0.0   # 0 = ευθεία, αρνητικό = αριστερά, θετικό = δεξιά
client.setCarControls(car_controls)

# Συλλογή εικόνων
n_images = 50   # πόσες εικόνες θέλεις
for i in range(n_images):
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
    ])

    if responses[0].width == 0:
        continue

    # Μετατροπή σε RGB
    img1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(responses[0].height, responses[0].width, 3)

    # Αποθήκευση με timestamp
    timestamp = time.strftime("%H%M%S")
    filename = os.path.join(output_folder, f"{scenario}_{i}_{timestamp}.jpg")
    cv2.imwrite(filename, img_rgb)

    print(f"[OK] Αποθηκεύτηκε: {filename}")
    time.sleep(0.1)  # μικρή καθυστέρηση για να μην τραβάει 60fps

# Σταμάτημα μετά τη συλλογή
car_controls.throttle = 0.0
client.setCarControls(car_controls)
client.enableApiControl(False)

print("[FINISHED] Συλλογή εικόνων ολοκληρώθηκε.")
