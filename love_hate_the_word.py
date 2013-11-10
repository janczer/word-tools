#!/usr/bin/env python
"""
Find examples of "I love/hate the word X" on Twitter and add them to Wordnik word lists.
"""
import word_tools

try: import timing # Optional, http://stackoverflow.com/a/1557906/724176
except: None

# Twitter: create an app at https://dev.twitter.com/apps/new
CONSUMER_KEY = "TODO_ENTER_YOURS_HERE"
CONSUMER_SECRET = "TODO_ENTER_YOURS_HERE"
OAUTH_TOKEN = "TODO_ENTER_YOURS_HERE"
OAUTH_SECRET = "TODO_ENTER_YOURS_HERE"

INI_FILE = "/Users/hugo/Dropbox/bin/data/lovehatetheword.ini"
CSV_FILE = "/Users/hugo/Dropbox/bin/data/lovehatetheword.csv"

love_max_id, hate_max_id = 0,0
STUFF = [
    ["I love the word", "I hate the word"], # search term
    [love_max_id, hate_max_id],
    ["twitter-loves", "twitter-hates"] # Wordnik word list permalink
    ]

# "I love the word X" or "X is my favourite new word"?
TARGET_WORD_FOLLOWS_SEARCH_TERM = True

# Test mode doesn't actually save csv, ini or update Wordnik or Twitter
TEST_MODE = False

if __name__ == '__main__':
    word_tools.init_twitter(OAUTH_TOKEN, OAUTH_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
    STUFF = word_tools.load_ini(INI_FILE, STUFF) # updates STUFF[1]

    for i,search_term in enumerate(STUFF[0]):
#         STUFF[1][i], words = get_words_from_twitter(search_term, STUFF[1][i])

        STUFF[1][i], results = word_tools.get_words_from_twitter(search_term, STUFF[1][i])
        words = word_tools.find_words(search_term, TARGET_WORD_FOLLOWS_SEARCH_TERM, results, CSV_FILE)

        if not TEST_MODE:
            word_tools.add_to_wordnik(words, STUFF[2][i])

        tweet_prefix = STUFF[0][i].replace("I ", "Tweeters ")
        if not TEST_MODE:
            word_tools.tweet_those(words, tweet_prefix)
        word_tools.save_ini(INI_FILE, STUFF)

# End of file