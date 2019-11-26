from django.shortcuts import HttpResponse
from django.views import View
from .tasks import load_files
from django.views.decorators.csrf import csrf_exempt
import json
import time
SECONDS_TO_WAIT = 1
FILES_LIST_ARGUMENT = "files_list"


def validate_content(content):
    """
    Validate the content of the request body - check if the are file names in the request body
    :param content: The request body
    :return: Boolean
    """
    if FILES_LIST_ARGUMENT in content:
        if len(content[FILES_LIST_ARGUMENT]) > 0:
            return True

    return False


@csrf_exempt
def etl_view(request):
    """
    A function view which checks if the request contain the file names if so calls the async function which load files
    :param request: The request containing the files list
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        content = json.loads(body_unicode)

        if validate_content(content):
            # load the files content into the DB
            result = load_files.delay(content[FILES_LIST_ARGUMENT])

            # Wait for the worker to finish the process
            while not result.ready():
                time.sleep(2)

            return HttpResponse(result.result)

    return HttpResponse(status=400)