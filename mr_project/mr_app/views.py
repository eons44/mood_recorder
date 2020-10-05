import json

from django.shortcuts import render

# Create your views here.
from time import time
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
import neo4j
from django.views.decorators.csrf import csrf_exempt
from requests import codes
from . import DRIVER, EMOTIONS, USERS
from datetime import datetime

#WRITE TRANSACTION FUNCTIONS
def create_user_tx(tx, name):
    result = tx.run('CREATE (u:User{name:$name}) RETURN u.name AS username', name=name)
    record = result.single()
    result.consume()
    return record['username']


def create_emotion_tx(tx, name):
    result = tx.run('CREATE (em:Emotion {name:$name})  RETURN em.name AS emotion_label', name=name)
    record = result.single()
    result.consume()
    return record['emotion_label']


def create_epoch_relationship_between_user_and_emotion(tx, emotion, user, epoch_timestamp):
    result = tx.run(f'MATCH (em:Emotion {{name:"{emotion}"}}), (u:User {{name:"{user}"}}) CREATE (u)-[ts:Timestamp{{epoch:"{epoch_timestamp}"}}]->(em) RETURN ts.epoch as seconds')
    record = result.single()
    result.consume()
    return record['seconds']


#EFFECTIVE READ TRANSACTIONS TO CHECK IF NODES EXIST OR NOT
def check_for_user(driver_arg, user_name):
    with driver_arg.session() as session:
        result = session.run("MATCH (n:User{ name:$user_name }) RETURN n.name AS name", user_name=user_name)
        values = result.values()
        if not values:
            return False
        else:
            return True


def check_for_emotion(driver_arg, emotion_name):
    with driver_arg.session() as session:
        result = session.run("MATCH (n:Emotion{ name:$emotion_name }) RETURN n.name AS name", emotion_name=emotion_name)
        values = result.values()
        if not values:
            return False
        else:
            return True


#FUNCTIONS THAT ACTUALLY CONNECT WITH THE DATABASE TO PERFORM TRANSACTIONS
def spawn_emotion_node(driver_arg, emotion):
    with driver_arg.session() as session:
        emotion_label = session.write_transaction(create_emotion_tx, emotion)
        print(emotion_label)


def spawn_user_node(driver_arg, username):
    with driver_arg.session() as session:
        user_name = session.write_transaction(create_user_tx, username)
        print(user_name)


def register_emotion(driver_arg, username, emotion):
    epoch_timestamp = time()
    with driver_arg.session() as session:
        seconds = session.write_transaction(create_epoch_relationship_between_user_and_emotion, emotion, username, epoch_timestamp)
        print(seconds)


def spawn_all_emotions(driver_arg, emotions_list):
    n_emotions = len(emotions_list)
    for i in range(n_emotions):
        spawn_emotion_node(driver_arg, emotions_list[i])


def add_users(driver_arg, users_list):
    n_users = len(users_list)
    for i in range(n_users):
        spawn_user_node(driver_arg, users_list[i])


@csrf_exempt
def create_user_emotion(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = ''
        emotion = ''

        try:
            user = body['user']
            emotion = body['emotion']
        except KeyError:
            return HttpResponseBadRequest('Missing required key')

        if check_for_user(DRIVER, user) and check_for_emotion(DRIVER, emotion):
            register_emotion(DRIVER, user, emotion)
        elif check_for_user(DRIVER, user):
            spawn_emotion_node(DRIVER, emotion)
            register_emotion(DRIVER, user, emotion)
        elif check_for_emotion(DRIVER, emotion):
            spawn_user_node(DRIVER, user)
            register_emotion(DRIVER, user, emotion)
        else:
            spawn_user_node(DRIVER, user)
            spawn_emotion_node(DRIVER, emotion)
            register_emotion(DRIVER, user, emotion)
        return HttpResponse(status=codes.created)

    return HttpResponseNotFound()


@csrf_exempt
def index(request, user_id, emotion):
    if request.method == 'POST':
        body = json.loads(request.body)
        asdf = body['asdf']
        return HttpResponse(f'you sent {asdf}')

    if request.method == 'GET':
        print(request.GET)
        return HttpResponse(f'you sent user_id = {user_id} and emotion = {emotion}')

    return HttpResponseNotFound()

    # return HttpResponse('''Hello, world! In the heavens above and on earth below, I alone will become the Honored One.<br/>
    #                     Add 'Udam-ecstatic' to the end of your URL to be an ecstatic Udam.<br/>
    #                     Add 'Udam-happy' to the end of your URL to be a happy Udam.<br/>
    #                     Add 'Udam-sad' to the end of your URL to be a sad Udam.<br/>
    #                     Add 'Udam-pissed' to the end of your URL to be a pissed Udam.<br/>
    #                     <br/>
    #                     Same for Rob and Taylor<br/>
    #                     <br/>
    #                     Add 'Python>C++' to be done.<br/>
    #                     Add 'bloob-bloob-bloob' to be eh.<br/>
    #                     Add 'Seon-the-Insayin' to the end of your URL to be the highest form of insanity in the universe.<br/>
    #                     Add 'beating-Seon' to the end of your url to be a pissed Robert Coleman Dalton III.''')
    #
    #
