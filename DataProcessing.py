"""
Title          : DataProcessing.py
Author         : Jasmeet Narang, Dimple Mehra
Description    : collecting and manipulating data to get meaningful processed data,
                 then storing it for further use

"""

import json
import tweepy
import time
from utils import consumer_key, consumer_secret, access_token, access_token_secret

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Setting your access token secret
auth.set_access_token(access_token, access_token_secret)

# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)

# get the followers of a particular user/ the main person that is center of the network
def get_followee(id,count):

    follow_ids = []

    try:
        cursor = tweepy.Cursor(api.friends_ids, user_id=id).items(count)
        for page in cursor:
                #print(page)
                follow_ids.append(page)
                time.sleep(1)
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")

    #follower_ids = [x for x in follower_ids]


    return follow_ids

# given user id get screen name
def get_screen_names(ids, user_id, user_screen_name):
    new_edges = []
    for id in ids:
        if (id[0] == user_id):
            u = user_screen_name
        else:
            try:
                t1 = api.get_user(id[0])
                u = t1.screen_name
            except tweepy.TweepError:
                print("Failed to run the command on that user, Skipping...")
        try:
            t2 = api.get_user(id[1])
        except tweepy.TweepError:
            print("Failed to run the command on that user, Skipping...")
        mytuple = (u, t2.screen_name)
        new_edges.append(mytuple)

    return new_edges


# get the friends of that particular person
def user_friends(user_id,all_follow,count,name):
    my_dict = {}
    overlap = []
    friends = []

    for s in all_follow:
        print("Person " + name + " follows: ", s)
        friend_follow_ids = get_followee(s,count)
        print("followee of ", s , " : ", friend_follow_ids)
        if user_id in friend_follow_ids:
            print(s, " follows ",user_id," back")
            my_dict[s] = friend_follow_ids
            mytuple = (user_id, s)
            friends.append(s)
            overlap.append(mytuple)

    return overlap, friends, my_dict


# finds friends of particular user/ main user that are friends with each other
def common_friends(user_and_followers):
    overlap = []
    processed = []
    for user in user_and_followers:
        #print(user)
        processed.append(user)
        followers = user_and_followers[user]
        #print(followers)
        for follower in followers:
            #print(follower)
            if follower not in processed:
                #print("in first is")
                #print(follower)
                #print('\n')
                if follower in user_and_followers and user in user_and_followers[follower]:
                    #print("second if")
                    #print(user, follower)
                    mytuple = (user, follower)
                    overlap.append(mytuple)

    return overlap

#store the edges in a text file
def store_data(edges,filename):
    with open(filename,'w') as f:
        json.dump(edges,f)

# read the edges
def read_data(filename):
    with open(filename,'r') as f:
        stored_edges = json.load(f)
    #print('in function')
    #print(stored_edges)
    return stored_edges

def save_dict(user_and_followees):
    user_and_followee = {}
    for k, v in user_and_followees.items():
        user_and_followee[int(k)] = [i for i in v]
    return user_and_followee

if __name__ == '__main__':
    name1 = 'KanganaTeam'
    u1 = api.get_user(name1)

    name2 = 'gssjodhpur'
    u2 = api.get_user(name2)

    name3 = 'AdnanSamiLive'
    u3 = api.get_user(name3)

    id1 = u1.id  #kangana = 3946905252
    print("Kangana Ranaut: " , id1)

    id2 = u2.id #Gajendra = 2371536685
    print("Gajendra Singh: ", id2)

    id3 = u3.id  # Adnan = 236826818
    print("Adnan Sami: ", id3)


    # Get followee of kangana, gajendra and adnan
    all_follow_kangana = get_followee(id1, 200)

    all_follow_gajendra = get_followee(id2, 200)

    all_follow_adnan = get_followee(id3, 200)


    #store the followee of kangana, gajendra and adnan
    store_data(all_follow_kangana, 'data/all_follow_kangana.txt')
    all_follow_kangana = read_data('data/all_follow_kangana.txt')

    store_data(all_follow_gajendra, 'data/all_follow_gajendra.txt')
    all_follow_gajendra = read_data('data/all_follow_gajendra.txt')

    store_data(all_follow_adnan, 'data/all_follow_adnan.txt')
    all_follow_adnan = read_data('data/all_follow_adnan.txt')


    # get followee of Kangana's followee
    overlap11, friends1, user_and_followee1 = user_friends(id1, all_follow_kangana, 70,name1)

    store_data(user_and_followee1, 'data/user_and_followee_Kangana.txt')
    user_and_followee1 = read_data('data/user_and_followee_Kangana.txt')
    store_data(overlap11, 'data/overlap11.txt')
    overlap11 = read_data('data/overlap11.txt')
    store_data(friends1, 'data/friends1.txt')
    friends1 = read_data('data/friends1.txt')


    # get followee of Gajendra's followee
    overlap12, friends2, user_and_followee2 = user_friends(id2, all_follow_gajendra, 70, name2)

    store_data(user_and_followee2, 'data/user_and_followee_Gajendra.txt')
    user_and_followee2 = read_data('data/user_and_followee_Gajendra.txt')
    store_data(overlap12, 'data/overlap12.txt')
    overlap12 = read_data('data/overlap12.txt')
    store_data(friends2, 'data/friends2.txt')
    friends2 = read_data('data/friends2.txt')


    # get followee of adnan's followee
    overlap13, friends3, user_and_followee3 = user_friends(id3, all_follow_adnan, 70, name3)

    store_data(user_and_followee3, 'data/user_and_followee_adnan.txt')
    user_and_followee3 = read_data('data/user_and_followee_adnan.txt')
    store_data(overlap13, 'data/overlap13.txt')
    overlap13 = read_data('data/overlap13.txt')
    store_data(friends3, 'data/friends3.txt')
    friends3 = read_data('data/friends3.txt')


    user_and_followee11 = {}
    user_and_followee11 = save_dict(user_and_followee1)
    user_and_followee22 = {}
    user_and_followee22 = save_dict(user_and_followee2)
    user_and_followee33 = {}
    user_and_followee33 = save_dict(user_and_followee3)

    # find connected neighbor's of Kangana, Gajendra and adnan
    overlap21 = common_friends(user_and_followee11)
    print("Kangana (Mutual Friends): ",overlap21)

    overlap22 = common_friends(user_and_followee22)
    print("Gajendra (Mutual Friends): ", overlap22)

    overlap33 = common_friends(user_and_followee33)
    print("Adnan (Mutual Friends): ", overlap33)


    edges1 = overlap11 + overlap21
    edges2 = overlap12 + overlap22
    edges3 = overlap13 + overlap33


    store_data(edges1, 'data/edges1.txt')
    stored_edges1 = read_data('data/edges1.txt')
    store_data(edges2, 'data/edges2.txt')
    stored_edges2 = read_data('data/edges2.txt')
    store_data(edges3, 'data/edges3.txt')
    stored_edges3 = read_data('data/edges3.txt')


    new_edges_kangana = get_screen_names(stored_edges1, u1, name1)
    new_edges_gajendra = get_screen_names(stored_edges2, u2, name2)
    new_edges_adnan = get_screen_names(stored_edges3, u3, name3)
    all_edges = new_edges_kangana+new_edges_gajendra+new_edges_adnan

    store_data(all_edges, 'data/screen_names.txt')
    all_edges = read_data('data/screen_names.txt')
    print(all_edges)
