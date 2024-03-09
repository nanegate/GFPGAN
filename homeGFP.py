import requests
import time
import json
import base64
import os
from PIL import Image
import subprocess
import io
# URL'yi ve passPc değerini değiştirin
url = "https://ai.plide.workers.dev/"
pass_pc_value = "eeKwp1RgzdlPZ6UOw9t6x4"
headersJson = {
    "Content-Type": "application/json"
}
while True:
    headers = {
        "passPc": pass_pc_value,
    }
    
    response = requests.get(url, headers=headers)
    print(response.text)
    data = json.loads(response.text)
    for item in data:
        headerUser = {
            "passid": item,
        }
        response = requests.get(url, headers=headerUser)
        folder_path = "userPhotos/"+item
        os.makedirs(folder_path, exist_ok=True)
        print(item)
        dataBase64 = json.loads(response.text)
        if dataBase64["active"] == True:
            decoded_data = base64.b64decode(dataBase64["base64Data"])
            file_path = os.path.join(folder_path, item+".jpeg")
            try:
                image = Image.open(io.BytesIO(decoded_data))
            except Exception as e:
                print(f"Error: Could not open image: {e}")
                
            image.save(file_path, "JPEG")
            print(f"Base64 data saved as JPEG image to: {file_path}")
            dataBase64["active"] = "false"
            dataBase64["randomId"] = item
            #print(dataBase64["base64Data"])
            print(dataBase64["active"])
            json_data = json.dumps(dataBase64)
            os.system(f"python inference_gfpgan.py -i userPhotos/{item}/ -o results -v 1.4 -s 2")
            image_path = "results/restored_imgs/"+item+".jpeg"
            image = Image.open(image_path)
            width, height = image.size
            aspect_ratio = width / height
            target_width = 800
            target_height = int(target_width / aspect_ratio)
            resized_image = image.resize((target_width, target_height))
            with io.BytesIO() as output:
                resized_image.save(output, format='JPEG', quality=100)  # 50% quality
                image_bytes = output.getvalue()
                base64_encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            print(base64_encoded_image)
            dataBase64["base64Data"] = base64_encoded_image
            json_data_kv = json.dumps(dataBase64)
            requests.post(url, headers=headerUser, data=json_data_kv)



    # İsteğin durum kodunu kontrol edin
    if response.status_code != 200:
        print(f"Hata: {response.status_code}")
        break

    # 10 saniye bekleyin
    time.sleep(10)

print("İşlem tamamlandı.")      
