from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import cv2
from detector.forms import ImageUploadForm
from PIL import Image
from django.contrib import messages


def calculate_bluriness(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var


def resize_image(image_path, width, height):
    img = Image.open(image_path)
    img_resized = img.resize((width, height), Image.LANCZOS)
    return img_resized


@login_required(login_url='/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            threshold = form.cleaned_data['threshold']
            instance.save()
            image_path = instance.image.path
            resized_image = resize_image(image_path, 500, 500)
            resized_image_path = image_path.replace('.png', '_resized.png')
            resized_image.save(resized_image_path)  # Save the resized image
            instance.image = 'images/' + resized_image_path.split('/')[-1]
            bluriness_level = calculate_bluriness(image_path)
            instance.bluriness_level = bluriness_level
            instance.is_blurry = bluriness_level < threshold
            instance.save()
            context = {
                'form': form,
                'image': instance,
            }
            return render(request, 'detect.html', context=context)
        else:
            messages.error(request, form.errors.as_data())
    else:
        form = ImageUploadForm(initial={'threshold': 100})
    return render(request, 'upload_image.html', {'form': form})
