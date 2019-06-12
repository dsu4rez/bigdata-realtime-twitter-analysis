package com.davidiscoding.flumetwittersource;
import java.util.HashMap;
import java.util.Map;

import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.EventDrivenSource;
import org.apache.flume.channel.ChannelProcessor;
import org.apache.flume.conf.Configurable;
import org.apache.flume.event.EventBuilder;
import org.apache.flume.source.AbstractSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import twitter4j.FilterQuery;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.conf.ConfigurationBuilder;
import twitter4j.json.DataObjectFactory;


public class TwitterSource extends AbstractSource
	implements EventDrivenSource, Configurable {
	
	private final static Logger logger = LoggerFactory.getLogger(TwitterSource.class);	

	private String consumerKey;
	private String consumerSecret;
	private String accessToken;
	private String accessTokenSecret;

	private String[] keywords;
	private long [] follows;
	private double [][] locations;

	private  TwitterStream twitterStream;


	@Override
	public void configure(Context context) {
		consumerKey = context.getString(TwitterSourceConstants.CONSUMER_KEY_KEY);
		consumerSecret = context.getString(TwitterSourceConstants.CONSUMER_SECRET_KEY);
		accessToken = context.getString(TwitterSourceConstants.ACCESS_TOKEN_KEY);
		accessTokenSecret = context.getString(TwitterSourceConstants.ACCESS_TOKEN_SECRET_KEY);
		
		TwitterQueryParameterParser tqpp = new TwitterQueryParameterParser();
		String keywordString = context.getString(TwitterSourceConstants.KEYWORDS_KEY, "");
		keywords = tqpp.getKeywords(keywordString);
		
		String followString = context.getString(TwitterSourceConstants.FOLLOW_IDS_KEY, "");
		follows = tqpp.getFollows(followString);
		
		String locationString = context.getString(TwitterSourceConstants.LOCATIONS_KEY, "");
		locations = tqpp.getLocations(locationString);
		
		ConfigurationBuilder cb = new ConfigurationBuilder();
		cb.setDebugEnabled(true)
		  .setOAuthConsumerKey(consumerKey)
		  .setOAuthConsumerSecret(consumerSecret)
		  .setOAuthAccessToken(accessToken)
		  .setOAuthAccessTokenSecret(accessTokenSecret)
		  .setJSONStoreEnabled(true);
	
		twitterStream = new TwitterStreamFactory(cb.build()).getInstance();
	}
	
	@Override
	public void start() {
    
		final ChannelProcessor channel = getChannelProcessor();
		final Map<String, String> headers = new HashMap<String, String>();
		
		StatusListener listener = new StatusListener(){
	        
			public void onStatus(Status status) {
	            System.out.println(status.getUser().getName() + " : " + status.getText());
	            logger.debug("Tweet arrived");

				headers.put("timestamp", String.valueOf(status.getCreatedAt().getTime()));
				Event event = EventBuilder.withBody(
						DataObjectFactory.getRawJSON(status).getBytes(), headers);

				channel.processEvent(event);
	        }
	        
	        public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}
	        public void onTrackLimitationNotice(int numberOfLimitedStatuses) {}
			public void onScrubGeo(long arg0, long arg1) { }
			public void onStallWarning(StallWarning arg0) { }
			
			public void onException(Exception ex) {
	            logger.error("Error while listening to Twitter stream.", ex);
	        }
	    };
	    
	    logger.debug("Setting up Twitter sample stream using consumer key" + consumerKey + 
				" and access token " + accessToken);
	    
	    twitterStream.addListener(listener);
	    
	    if (keywords.length == 0 && follows.length == 0 && locations.length == 0) {
			logger.debug("Starting up Twitter sampling...");
			twitterStream.sample();
			
		} else {
			logger.debug("Starting up Twitter filtering...");
			
			FilterQuery query = new FilterQuery();
			if (keywords.length > 0) query.track(keywords);
		    if (follows.length > 0) query.follow(follows);
		    if (locations.length > 0) query.locations(locations);
			
			twitterStream.filter(query);
		}
		
		super.start();

	}


	@Override
	public void stop() {
		logger.debug("Shutting down Twitter sample stream...");
		twitterStream.shutdown();
		super.stop();
	}
}