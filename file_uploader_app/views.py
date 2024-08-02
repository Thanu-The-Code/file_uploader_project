from django.shortcuts import render
from django.conf import settings
import os

from .forms import UploadForm
from .uploader import FileUploader

def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            directory = form.cleaned_data['directory']
            aws_access_key = settings.AWS_ACCESS_KEY_ID
            aws_secret_key = settings.AWS_SECRET_ACCESS_KEY
            s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            gcs_bucket_name = settings.GS_BUCKET_NAME
            s3_file_types = settings.S3_FILE_TYPES
            gcs_file_types = settings.GCS_FILE_TYPES
            
            try:
                uploader = FileUploader(aws_access_key, aws_secret_key, s3_bucket_name, gcs_bucket_name)
                uploader.upload_files(directory, s3_file_types, gcs_file_types)
                return render(request, 'file_uploader/upload_successfull.html')
            except Exception as e:
                
                print(f"Error: {e}")
                return render(request, 'file_uploader/upload_error.html', {'error': str(e)})
    else:
        form = UploadForm()

    return render(request, 'file_uploader/upload.html', {'form': form})
