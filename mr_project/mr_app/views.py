import json
from json import JSONDecodeError

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import codes

from . import DRIVER
from .neo4j_transactions import *


@csrf_exempt
def get_user_emotion(request):
    if request.method == 'GET':
        user = ''
        emotion = ''

        try:
            user = request.GET['user']
        except KeyError:
            return HttpResponseBadRequest('Missing required "user" key')

        try:
            emotion = request.GET['emotion']
        except KeyError:
            return HttpResponseBadRequest('Missing required "emotion" key')

        if check_for_user(DRIVER, user) and check_for_emotion(DRIVER, emotion):
            return JsonResponse(fetch_epochs_of_user_emotion_pair(DRIVER, user, emotion))

        # change these to HttpResponseNotFound instead of HttpResponseBadRequest
        if check_for_user(DRIVER, user):
            return HttpResponseNotFound('Slow down dawg! The emotion does not exist, ya need a spelling lesson?')

        if check_for_emotion(DRIVER, emotion):
            return HttpResponseNotFound('Slow down dawg! The user does not exist, ya need a spelling lesson?')

        return HttpResponseNotFound('Slow down dawg! The user and emotion do not exist, ya need a spelling lesson?')

    return HttpResponseNotFound()


@csrf_exempt
def get_all_user_emotions(request):
    if request.method == 'GET':
        user = ''
        try:
            user = request.GET['user']
        except KeyError:
            return HttpResponseBadRequest('Missing required "user" key')

        if check_for_user(DRIVER, user):
            return JsonResponse(fetch_all_emotions_and_epochs_of_user(DRIVER, user))
        return HttpResponseNotFound('Slow down dawg! The user does not exist, ya need a spelling lesson?')

    return HttpResponseNotFound()


@csrf_exempt
def create_user_emotion(request):
    if request.method == 'POST':
        body = {}
        user = ''
        emotion = ''

        try:
            body = json.loads(request.body)
        except JSONDecodeError:
            return HttpResponseBadRequest('Payload received was not a JSON')

        try:
            user = body['user']
        except KeyError:
            return HttpResponseBadRequest('Missing required "user" key')

        try:
            emotion = body['emotion']
        except KeyError:
            return HttpResponseBadRequest('Missing required "emotion" key')

        if not check_for_user(DRIVER, user):
            spawn_user_node(DRIVER, user)

        if not check_for_emotion(DRIVER, emotion):
            spawn_emotion_node(DRIVER, emotion)

        register_emotion(DRIVER, user, emotion)

        return HttpResponse(status=codes.created)

    return HttpResponseNotFound()


@csrf_exempt
def index(request, user_id, emotion):
    if request.method == 'POST':
        return HttpResponse('From the heavens above to the Earth below, I alone will become the honored one.')

    if request.method == 'GET':
        return HttpResponse('From the heavens above to the Earth below, I alone will become the honored one.')

    return HttpResponseNotFound()
