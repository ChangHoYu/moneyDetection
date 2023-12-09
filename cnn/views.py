from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import CNNModel

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)

        prediction = CNNModel.predict_image(f'media/{image_path}')

        if int(prediction[0][0]) == 1 :
            prediction = '10000원'
        elif int(prediction[0][1]) == 1 :
            prediction = '1000엔'
        elif int(prediction[0][2]) == 1 :
            prediction = '1000원'
        elif int(prediction[0][3]) == 1 :
            prediction = '10000대만달러'
        elif int(prediction[0][4]) == 1 :
            prediction = '10000동'
        elif int(prediction[0][5]) == 1 :
            prediction = '10유로'
        elif int(prediction[0][6]) == 1 :
            prediction = '20바트'
        elif int(prediction[0][7]) == 1 :
            prediction = '2달러'
        elif int(prediction[0][8]) == 1 :
            prediction = '5000엔'
        elif int(prediction[0][9]) == 1 :
            prediction = '오천원'
        elif int(prediction[0][10]) == 1 :
            prediction = '500동'
        elif int(prediction[0][11]) == 1 :
            prediction = '50유로'

        return render(request, 'cnn/result.html', {'prediction': prediction})

    return render(request, 'cnn/upload_image.html')
