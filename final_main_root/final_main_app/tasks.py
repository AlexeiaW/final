from celery import shared_task
from .models import *
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile

# Create a thumbnail version of the uploaded image
@shared_task
def make_thumbnail(record_pk, appuser_pk):
    appuser = AppUser.objects.get(pk=appuser_pk)
    record = Image.objects.get(pk=record_pk)
    record.user = appuser

    image = img.open('images/'+str(record.image))
    x_scale_factor = image.size[0]/100
    thumbnail = image.resize((100, int(image.size[1]/x_scale_factor)))
    # thumbnail.save("test.jpg")

    byteArr = io.BytesIO()
    thumbnail.save(byteArr, format='jpeg')
    file = SimpleUploadedFile("thumb_"+str(record.image), byteArr.getvalue())
    record.thumbnail = file
    record.save()
