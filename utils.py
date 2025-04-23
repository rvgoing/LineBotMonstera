import tensorflow as tf
from PIL import Image
import numpy as np
import io
from io import BytesIO


# 定義你的類別對應
classes = ['曬傷', '正常龜背芋', '爛根加老化', '病菌感染', '非龜背芋']


# 載入 TFLite 模型
interpreter = tf.lite.Interpreter(model_path="best_model_fp16.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))  # 根據你訓練模型的輸入大小調整
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(image_bytes):
    input_data = preprocess_image(image_bytes)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_label = np.argmax(output)
    confidence = np.max(output)
    return predicted_label, confidence



# 👇 這就是你問的函式，可以貼在 LineBotAI.py 裡
def predict_image_from_bytes(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    input_data = np.expand_dims(img_array, axis=0)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])[0]
    label_index = int(np.argmax(output))
    confidence = float(np.max(output))
    label = classes[label_index]

    return label, confidence