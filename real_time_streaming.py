from slistener import SListener
import time, tweepy, sys

consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def main():
    track = ['obama', 'romney']

    listen = SListener(api, 'myprefix')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try:
        stream.filter(track=track)
    except:
        print "error!"
        stream.disconnect()


if __name__ == '__main__':
    main()