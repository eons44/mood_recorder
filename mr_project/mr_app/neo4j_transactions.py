from time import time


def create_node_transaction(tx, label, property, property_value):
    tx.run(f'CREATE (node:{label} {{{property}: "{property_value}"}})')


def create_epoch_relationship_between_user_and_emotion(tx, emotion, user, epoch_timestamp):
    tx.run(f'MATCH (em:Emotion {{name:"{emotion}"}}), (u:User {{name:"{user}"}}) CREATE (u)-[ts:Timestamp{{epoch:"{epoch_timestamp}"}}]->(em) RETURN ts.epoch as seconds')


#EFFECTIVE READ TRANSACTIONS TO CHECK IF NODES EXIST OR NOT
def get_node(driver, label, property, property_value):
    with driver.session() as session:
        return session.run(f'MATCH (node:{label}{{ {property}: "{property_value}" }}) RETURN node.{property} as {property}').values()


def check_for_user(driver, username):
    return True if get_node(driver, 'User', 'name', username) else False


def check_for_emotion(driver, emotion_name):
    return True if get_node(driver, 'Emotion', 'name', emotion_name) else False


def fetch_epochs_of_user_emotion_pair(driver_arg, user_name, emotion_name):
    with driver_arg.session() as session:
        result = session.run('''MATCH (u)-[ts]->(em) WHERE u.name = $user_name AND em.name = $emotion_name RETURN 
                             ts.epoch AS timestamps''', user_name=user_name, emotion_name=emotion_name)
        return {
            'emotion': emotion_name,
            'timestampList': [record['timestamps'] for record in result]
            }


def fetch_all_emotions_of_one_user(driver_arg, user_name):
    with driver_arg.session() as session:
        result = session.run('''MATCH (u)-->(em) WHERE u.name = $user_name  RETURN 
                             em.name AS emotions''', user_name=user_name)
        return set([record['emotions'] for record in result])


def fetch_all_emotions_and_epochs_of_user(driver_arg, user_name):
    emotions_of_user = fetch_all_emotions_of_one_user(driver_arg, user_name)

    return {
        'user': user_name,
        'emotionList': [fetch_epochs_of_user_emotion_pair(driver_arg, user_name, emotion) for emotion in emotions_of_user]
    }


#FUNCTIONS THAT ACTUALLY CONNECT WITH THE DATABASE TO PERFORM TRANSACTIONS
def spawn_emotion_node(driver_arg, emotion):
    with driver_arg.session() as session:
        emotion_label = session.write_transaction(create_node_transaction, 'Emotion', 'name', emotion)
        print(emotion_label)


def spawn_user_node(driver_arg, username):
    with driver_arg.session() as session:
        user_name = session.write_transaction(create_node_transaction, 'User', 'name', username)
        print(user_name)


def register_emotion(driver_arg, username, emotion):
    epoch_timestamp = time()
    with driver_arg.session() as session:
        seconds = session.write_transaction(create_epoch_relationship_between_user_and_emotion, emotion, username, epoch_timestamp)
        print(seconds)


