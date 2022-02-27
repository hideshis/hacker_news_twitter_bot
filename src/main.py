import requests
import tweepy

def tweet(tweet_message):
    # 認証に必要なキーとトークン
    API_KEY = 'XXXXXXXXXXXXXXX'
    API_SECRET = 'XXXXXXXXXXXXXXX'
    ACCESS_TOKEN = 'XXXXXXXXXXXXXXX'
    ACCESS_TOKEN_SECRET = 'XXXXXXXXXXXXXXX'

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(tweet_message)

def get_500_top_and_new_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    story_id_list = response.json()

    return story_id_list

def filter_qa_related_stories(story_id_list):
    counter = 0

    for story_id in story_id_list:
        url = "https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json?print=pretty"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        story_detail = response.json()
        story_id = str(story_detail["id"])
        story_title = story_detail["title"]
        story_title_lower = story_title.lower()
        try:
            story_url = story_detail["url"]
        except KeyError:
            story_url = "https://news.ycombinator.com/item?id=" + story_id
        print(str(story_id) + story_title + "|" + story_url)

        if ("qa" in story_title_lower) or ("quality" in story_title_lower) or ("bug" in story_title_lower) or ("test" in story_title_lower):
            tweet_message = story_title + " " + story_url
            print("    " + tweet_message)
            tweet(tweet_message)

        counter += 1
        if counter == 100:
            break


story_id_list = get_500_top_and_new_stories()
print(len(story_id_list))
filter_qa_related_stories(story_id_list)
