import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import StorageLevel
import json
from textblob import TextBlob
import requests


def analyze_sentiment(text):
    testimonial = TextBlob(text)
    return testimonial.sentiment.polarity


def get_sentiment_tuple(sent):
    neutral_threshold = 0.05
    if sent >= neutral_threshold:       # positive
        return (0, 0, 1)
    elif sent > -neutral_threshold:     # neutral
        return (0, 1, 0)
    else:                               # negative
        return (1, 0, 0)


def get_top_keywords(dstream_tweets_sentiment_analysed, starts_with, window_length, sliding_interval):

    topics = dstream_tweets_sentiment_analysed. \
        map(lambda (user, text, sent): ((user, sent), text)). \
        flatMapValues(lambda text: text.split(" ")). \
        filter(lambda (kp, w): len(w) > 1 and w[0] == starts_with). \
        map(lambda ((user, sent), t): (t, (1, sent)))

    topics_count_acc_sent = topics. \
        reduceByKeyAndWindow(lambda (c1, s1), (c2, s2): (c1+c2, (s1[0]+s2[0], s1[1]+s2[1], s1[2]+s2[2])), None,
                             window_length, sliding_interval)

    sorted_topics = topics_count_acc_sent. \
        map(lambda (t, (count, sent)): (count, (t, sent))). \
        transform(lambda rdd: rdd.sortByKey(False)). \
        map(lambda (count, (t, sent)): (t, (count, sent)))

    return sorted_topics


def get_most_active_users(dstream_tweets_sentiment_analysed, window_length, sliding_interval):

    topics = dstream_tweets_sentiment_analysed. \
        map(lambda (user, text, sent): (user, (1, sent)))

    user_count_acc_sent = topics. \
        reduceByKeyAndWindow(lambda (c1, s1), (c2, s2): (c1 + c2, (s1[0] + s2[0], s1[1] + s2[1], s1[2] + s2[2])), None,
                             window_length, sliding_interval)

    sorted_users = user_count_acc_sent. \
        map(lambda (user, (count, sent)): (count, (user, sent))). \
        transform(lambda rdd: rdd.sortByKey(False)). \
        map(lambda (count, (user, sent)): (user, (count, sent)))

    return sorted_users


def get_twitter_analysis_counters(dstream_tweets_sentiment_analysed, window_length, sliding_interval):

    tweets_to_count = dstream_tweets_sentiment_analysed. \
        map(lambda (user, text, sent): ('count', (1, sent)))

    tweets_count_acc_sent = tweets_to_count. \
        reduceByKeyAndWindow(lambda (c1, s1), (c2, s2): (c1 + c2, (s1[0] + s2[0], s1[1] + s2[1], s1[2] + s2[2])), None,
                             window_length, sliding_interval)

    total_count = tweets_count_acc_sent. \
        map(lambda (k, (count, sent)): (count, sent))

    return total_count


def send_top_to_dashboard(dstream_tweets_sentiment_analysed, url):

    num = 10

    def take_and_send(time, rdd):
        if not rdd.isEmpty():
            taken = rdd.take(num)

            labels = []
            negative = []
            neutral = []
            positive = []
            for (name, (count, (neg, neu, pos))) in taken:
                labels.append(name)
                negative.append(neg)
                neutral.append(neu)
                positive.append(pos)

            request_data = {'label': str(labels), 'negative': str(negative), 'neutral': str(neutral), 'positive': str(positive)}
            response = requests.post(url, data=request_data)

    dstream_tweets_sentiment_analysed.foreachRDD(take_and_send)


def send_counters_to_dashboard(dstream_tweets_sentiment_analysed, url):

    def take_and_send(time, rdd):
        if not rdd.isEmpty():
            (total, (negative, neutral, positive)) = rdd.first()

            request_data = {'total': total, 'negative': negative, 'neutral': neutral, 'positive': positive}
            response = requests.post(url, data=request_data)

    dstream_tweets_sentiment_analysed.foreachRDD(take_and_send)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: tending_topics.py <kafka-topic>"
        sys.exit(-1)

    topic = sys.argv[1]

    sc = SparkContext()
    sc.setLogLevel("ERROR")

    batch_interval = 2
    window_length = 15*60
    sliding_interval = 6

    ssc = StreamingContext(sc, batch_interval)

    ssc.checkpoint("twittercheckpt")

    twitterKafkaStream = KafkaUtils. \
        createDirectStream(ssc, [topic], {"metadata.broker.list": "quickstart.cloudera:9092"})

    tweets = twitterKafkaStream. \
        map(lambda (k, v): json.loads(v)). \
        map(lambda json_object: (json_object["user"]["screen_name"], json_object["text"]))

    tweets_sentiment_analysed = tweets. \
        map(lambda (user, text): (user, text, get_sentiment_tuple(analyze_sentiment(text))))

    tweets_sentiment_analysed.persist(StorageLevel.MEMORY_AND_DISK)

    top_topics = get_top_keywords(tweets_sentiment_analysed, '#', window_length, sliding_interval)
    top_mentioned = get_top_keywords(tweets_sentiment_analysed, '@', window_length, sliding_interval)
    top_users = get_most_active_users(tweets_sentiment_analysed, window_length, sliding_interval)

    server = 'http://localhost:5001/'
    send_top_to_dashboard(top_topics, server + 'update_most_used_hashtags')
    send_top_to_dashboard(top_mentioned, server + 'update_most_mentioned_users')
    send_top_to_dashboard(top_users, server + 'update_most_active_users')

    tweet_counters = get_twitter_analysis_counters(tweets_sentiment_analysed, window_length, sliding_interval)
    send_counters_to_dashboard(tweet_counters, 'update_tweet_counters')

    ssc.start()
    ssc.awaitTermination()
