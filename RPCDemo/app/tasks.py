from __future__ import absolute_import, unicode_literals
from celery import shared_task
import random
from .models import FileTable
import os


@shared_task
def load_files(files_list):
    """
    For each file try to read the file, is possible than save it in the database.
    """
    for file_path in files_list:
        try:
            if os.path.isfile(file_path):
                file_name = file_path.split('\\')[-1]

                content = None

                # Read the file
                with file_path as f:
                    content = f.read()

                    # Save the file name to the DB
                    new_file = FileTable(name=file_name, content=content)
                    new_file.save()
        except Exception as e:
            print(str(e))

    return 'Process finished'
