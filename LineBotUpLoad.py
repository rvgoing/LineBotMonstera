import os
import sys
import requests
from io import BytesIO
from flask import Flask, request, abort
from PIL import Image
import torch
from torchvision import models, transforms
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage


# Initialize Flask app
app = Flask(__name__)

# LINE Bot credentials from the LINE Developers Console
# CHANNEL_SECRET = 'LINE_CHANNEL_SECRET'  # Replace with your Channel Secret
# CHANNEL_ACCESS_TOKEN = 'LINE_CHANNEL_ACCESS_TOKEN'  # Replace with your Channel Access Token

# CHANNEL_ACCESS_TOKEN = "3v0P0QKM6SK5EtmW4tyzBZRgbenxgXjm9zNvPDvgOYZJRN/Z7gDp76rhOIMO/v/qmlZf6XFQGBlBC0v5sYPxcfU1JPl3i7ruOGNLn94HZgJZtnZbTojfwGANyD0Dy9rCNIH2HFXSYE9C90DMLsyjVAdB04t89/1O/w1cDnyilFU="
# CHANNEL_SECRET = "79bffdb9e50e19336e79aad0679665fc"

# Initialize LINE Bot API and Handler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


# 載入模型和類別名稱
MODEL_PATH = 'convnext_tiny_best.pth'
checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

# 初始化模型架構
model = models.convnext_tiny(weights=None)
model.classifier[2] = torch.nn.Linear(model.classifier[2].in_features, len(checkpoint['class_names']))
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 類別名稱自動取得
class_names = checkpoint['class_names']

# 預處理流程
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def predict_image(image):
    img = image.convert("RGB")
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        confidence, predicted_class = torch.max(probabilities, 0)

    label = class_names[predicted_class.item()]
    return label, confidence.item()


# Webhook for receiving LINE events
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        abort(400)

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200



@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 取得圖片內容
    message_content = line_bot_api.get_message_content(event.message.id)
    image = Image.open(BytesIO(message_content.content))

    # 進行預測
    label, confidence = predict_image(image)

    # 回傳結果給使用者
    reply_text = f"預測類別：{label}\n信心值：{confidence * 100:.2f}%"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


# def callback():
#     # Get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']

#     # Get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # Verify the signature and handle the request
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK',200

# Event handler for text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Reply with a simple text message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello, this is a simple LINE Bot demo!')
    )

if __name__ == "__main__":
    # Run Flask app
    app.run(debug=True, port=5000)
