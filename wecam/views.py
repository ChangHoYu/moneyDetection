from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import torch
import torchvision.models as models
from ultralytics import YOLO
from django.core.files.storage import FileSystemStorage



def process_image(request):
    
# 파인 튜닝된 가중치 로드
    yolo_model = YOLO('wecam/best.pt')
    if request.method == 'POST' and request.FILES['image']:
        # 이미지 업로드
        # image = request.FILES['image']
        # image_path = default_storage.save('uploaded_images/' + image.name, ContentFile(image.read()))
        uploaded_image = request.FILES['image']
        image_path = save_uploaded_image(uploaded_image)
        prediction = yolo_model(image_path)
        
        # 예측 결과를 템플릿으로 전달
        output_image_path = draw_boxes_on_image(image_path, prediction)
        for r in prediction :
            if int(r.boxes.cls[0].tolist()) == 0 :
                prediction = '1000원'
            elif int(r.boxes.cls[0].tolist()) == 1 :
                prediction = '5000원'
            elif int(r.boxes.cls[0].tolist()) == 2 :
                prediction = '10000원'
            elif int(r.boxes.cls[0].tolist()) == 3 :
                prediction = '20달러'
            elif int(r.boxes.cls[0].tolist()) == 4 :
                prediction = '500동' 
        return render(request, 'webcam/yoloresult.html', {'prediction': prediction, 'image_path': output_image_path})
    return render(request, 'webcam/upload_image.html') 

def save_uploaded_image(uploaded_image):
    # 이미지 저장 및 경로 반환
    fs = FileSystemStorage()
    image_path = fs.save(uploaded_image.name, uploaded_image)
    return f'media/{image_path}'

def draw_boxes_on_image(image_path, prediction):
    # 이미지에 박스를 그려 저장하고, 새로운 이미지의 경로를 반환
    # 이 부분은 실제로 Pillow 라이브러리를 사용하여 구현해야 합니다.
    # Pillow를 사용하여 탐지된 객체 주위에 박스를 그리는 방법은 아래와 같이 될 수 있습니다.
    from PIL import Image, ImageDraw

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for pred_item in prediction:  # xyxy를 통해 좌표를 얻음
        try:
            boxes = pred_item.boxes
            if boxes is not None:
                box = boxes.xyxy[0].tolist()  # Tensor를 리스트로 변환
                draw.rectangle([box[0], box[1], box[2], box[3]], outline="red", width=5)
        except AttributeError:
            # 'boxes' 속성이 없는 경우 예외 처리
            pass

    output_image_path = image_path.replace("media/", "media/result_")
    img.save(output_image_path)
    return output_image_path