# bigdata-realtime-twitter-analysis
Personal project where I perform some analytics (including Sentiment Analysis) over a Twitter Stream using Big Data Technologies of the Hadoop echosystem such as Flume, Kafka, and Spark Streaming.

![Project Architecture](http://davidiscoding.com/wp-content/uploads/2019/06/Screenshot-2019-06-11-at-11.07.57-1024x582.png)

If you want to know more about this project, you can see a detailed explanation in my persoanal blog [here](http://davidiscoding.com/real-time-twitter-sentiment-analysis-pt-1-introduction).

This Git repository contains:
- Flume 
  - Custom Components to Stream and Filter Tweets (Custom Event Driven Source and Custom Interceptor)
  - Flume Agent Configuration File
  
- Spark Streaming: Code in Python for a real-time Twitter sentiment analysis using TextBlob (PyCharm Project)

- Dashboard: Flask Web Application for displaying the results using Chart.js (PyCharm Project)
