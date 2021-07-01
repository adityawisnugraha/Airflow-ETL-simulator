"""Tweet Processor

The transform part in ETL process.
This script is used to transform tweet object,
from original form as returned by the API
to objects defined by data model.

"""

"""
Notes
Tweet data dictionary
1. created_at					: String
2. id							: Int64
3. id_str						: String
4. text 						: String
5. source						: String (HTML-formatted)
6. truncated					: Boolean (true/false)
7. in_reply_to_status_id		: Int64, Nullable
8. in_reply_to_status_id_str	: String, Nullable
9. in_reply_to_user_id			: Int64, Nullable
10. in_reply_to_user_id_str		: String, Nullable
11. in_reply_to_screen_name		: String, Nullable
12. user 						: {User object}
13. coordinates					: {Coordinates object}, Nullable
14. place						: {Places}, Nullable
15. quoted_status_id*			: Int64
16. quoted_status_id_str*		: String
17. is_quote_status				: Boolean (true/false)
18. quoted_status* 				: {Tweet} 
19. retweeted_status*			: {Tweet}
20. reply_count					: Int
21. retweet_count				: Int
22. favorite_count				: Int
23. entities					: {Entities}
24. extended_entities			: {Extended Entities}
25. favorited					: Boolean
26. retweeted 					: Boolean
27. possibly_sensitive			: Boolean
28. filter_level				: String
29. lang						: String, nullable BCP 47
"""
import re
from datetime import datetime
import json

class TweetDataExtractor():
	"""Extract data from tweet object"""
	
	def __init__(self, tweet_dict):
		self.tweet_dict = tweet_dict
		self.main_tweet = None
		self.user_data = None
		self.rt_data = None
		self.quote_data = None
		self.media = None
		self.hashtag = None
		self.url = None
		self.place = None

	@staticmethod
	def get_app_source(source_str):
		"""get app source data from tweet object
		by getting string between the html tag
		"""
		found = re.findall(">(.*)<",source_str)
		if len(found)==0: #if string can't be found by the regex pattern
			return source_str #return original source string
		else:
			return found[0]

	@staticmethod
	def get_text(tweet_dict):
		"""get the tweet (status), the main data of tweet
		text can be present in full_text,extended_tweet, or tweet
		key
		"""
		if "full_text" in tweet_dict:
			return tweet_dict["full_text"].replace('\x00'," ") #remove null object
		elif "extended_tweet" in tweet_dict:
			return tweet_dict['extended_tweet']['full_text'].replace('\x00'," ")
		else:
			return tweet_dict['text'].replace('\x00'," ")

	@staticmethod
	def process_date(dateobj):
		"""parse string to python datetime object
		"""
		date_str = datetime.strptime(dateobj,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
		return date_str	

	def get_main_tweet(self):
		"""get "main" tweet object for retweet/quote tweet. 
		Main tweet is retweeted/quoted tweet.
		"""
		if "retweeted_status" in self.tweet_dict:
			entry = self.tweet_dict['retweeted_status']
		elif "quoted_status" in self.tweet_dict:
			entry = self.tweet_dict['quoted_status']
		else:
			entry = self.tweet_dict

		#print(entry.keys())

		id = entry['id']
		id_str = entry['id_str']
		user_id = entry['user']['id']
		created_at = entry['created_at']
		text = self.get_text(entry)
		source = self.get_app_source(entry['source'])
		truncated = entry['truncated']
		lang = entry['lang']
		retweet_count = entry['retweet_count']
		try:
			quote_count = entry['quote_count']
		except KeyError:
			quote_count = 0
		try:
			reply_count = entry['reply_count']
		except Exception as e:
			reply_count = 0
		in_reply_to_status_id = entry['in_reply_to_status_id']
		in_reply_to_status_id_str =entry['in_reply_to_status_id_str']
		in_reply_to_user_id = entry['in_reply_to_user_id']
		in_reply_to_user_id_str = entry['in_reply_to_user_id_str']
		main_tweet ={
			'id': id,
			'id_str': id_str,
			'user_id': user_id,
			'created_at': created_at,
			'text': text,
			'source': source,
			'truncated': truncated,
			'lang': lang,
			'retweet_count': retweet_count,
			'quote_count': quote_count,
			'reply_count': reply_count,
			'in_reply_to_status_id': in_reply_to_status_id,
			'in_reply_to_status_id_str': in_reply_to_status_id_str,
			'in_reply_to_user_id': in_reply_to_user_id,
			'in_reply_to_user_id_str': in_reply_to_user_id_str
		}
		return main_tweet

	def get_rt_data(self):
		"""Get the data of the parent tweet,
		the retweeted tweet is processed with
		get_main_tweet
		"""
		try:
			tweet_id = self.tweet_dict["id"]
			retweeted_id = self.tweet_dict["retweeted_status"]["id"]
			retweet_user = self.tweet_dict["user"]["id"]
			retweet_text = self.get_text(self.tweet_dict)
			#retweet_hashtag = self.tweet_dict[""]
		except Exception as e:
			raise e
		rt_data = {
			'tweet_id' : tweet_id,
			'retweeted_id' : retweeted_id,
			'retweet_user' : retweet_user,
			'retweet_text' : retweet_text
		}
		return rt_data

	def get_quote_data(self):
		"""Get the data of the parent tweet,
		the quoted tweet is processed with
		get_main_tweet
		"""
		try:
			tweet_id = self.tweet_dict["id"]
			quoted_id = self.tweet_dict["quoted_status"]["id"]
			quoted_user = self.tweet_dict["user"]["id"]
			quoted_text = self.get_text(self.tweet_dict)
			#quoted_hashtag =
		except Exception as e:
			raise e
		quote_data = {
			'tweet_id' : tweet_id, 
			'quoted_id' : quoted_id,
			'quoted_user' : quoted_user,
			'quoted_text' : quoted_text
		}
		return quote_data

	def get_user(self):
		"""get user data of parent tweet
		"""

		deleted_key=["entities",
		"time_zone",
		"profile_background_image_url_https",
		"is_translation_enabled",
		"profile_banner_url",
		"has_extended_profile"]
		for key in deleted_key:
			try:
				del self.tweet_dict["user"][key]
			except KeyError:
				continue
		description = self.tweet_dict["user"]["description"]
		name = self.tweet_dict["user"]["name"]
		location = self.tweet_dict["user"]["location"]
		self.tweet_dict["user"]["description"] = description.replace('\x00'," ")
		self.tweet_dict["user"]["name"] = name.replace('\x00'," ")
		self.tweet_dict["user"]["location"] = location.replace('\x00'," ")
		return self.tweet_dict["user"]

	def get_user_from_main_tweet(self):
		"""get user data from quoted
		and retweeted tweet
		"""

		if "retweeted_status" in self.tweet_dict:
			entry = self.tweet_dict['retweeted_status']
		elif "quoted_status" in self.tweet_dict:
			entry = self.tweet_dict['quoted_status']
		deleted_key=["entities",
		"time_zone",
		"profile_background_image_url_https",
		"is_translation_enabled",
		"profile_banner_url",
		"has_extended_profile"]
		for key in deleted_key:
			try:
				del entry["user"][key]
			except KeyError:
				continue
		description = entry["user"]["description"]
		name = entry["user"]["name"]
		entry["user"]["description"] = description.replace('\x00'," ")
		entry["user"]["name"] = name.replace('\x00'," ")
		return entry["user"]

	def get_hashtags(self,main=True):
		"""
		return list of hashtags dict
		"""
		if main:
			if "retweeted_status" in self.tweet_dict:
				entry = self.tweet_dict['retweeted_status']
			elif "quoted_status" in self.tweet_dict:
				entry = self.tweet_dict['quoted_status']
			else:
				entry = self.tweet_dict
		else:
			entry = self.tweet_dict
		entities = entry['entities']
		if "hashtags" in entities and len(entities["hashtags"])>0:
			ht = {"tweet_id" : entry['id']}
			ht["hashtag"] = json.dumps(entities["hashtags"])
			return ht
		else :
			return

	def get_symbol(self,main=True):
		"""
		return list of symbol dict
		"""
		if main:
			if "retweeted_status" in self.tweet_dict:
				entry = self.tweet_dict['retweeted_status']
			elif "quoted_status" in self.tweet_dict:
				entry = self.tweet_dict['quoted_status']
			else:
				entry = self.tweet_dict
		else:
			entry = self.tweet_dict
		entities = entry['entities']
		if "symbols" in entities and len(entities["symbols"])>0:
			sym = {"tweet_id" : entry['id']}
			sym["symbol"] = json.dumps(entities["symbols"])
			return sym
		else :
			return
		
	def get_mention_user(self,main=True):
		if main:
			if "retweeted_status" in self.tweet_dict:
				entry = self.tweet_dict['retweeted_status']
			elif "quoted_status" in self.tweet_dict:
				entry = self.tweet_dict['quoted_status']
			else:
				entry = self.tweet_dict
		else:
			entry = self.tweet_dict
		entities = entry['entities']
		if "user_mentions" in entities:
			# user_mentions_list = []
			for item in entities['user_mentions']:
				try:
					del item["indices"]
				except KeyError:
					pass
				finally:
					item["tweet_id"] = entry['id']
					# user_mentions_list.append(item)
				yield item
			# return user_mentions_list
		else:
			return 

	def get_media(self,main=True):
		if main:
			if "retweeted_status" in self.tweet_dict:
				entry = self.tweet_dict['retweeted_status']
			elif "quoted_status" in self.tweet_dict:
				entry = self.tweet_dict['quoted_status']
			else:
				entry = self.tweet_dict
		else:
			entry = self.tweet_dict
		entities = entry['entities']
		if "media" in entities:
			# media_list = []
			for item in entities['media']:
				deleted_key=["indices",
				"sizes",
				"source_status_id",
				"source_status_id_str",
				"url",
				"source_user_id",
				"source_user_id_str"
				]
				for key in deleted_key:
					try:
						del item[key]
					except KeyError:
						continue
				item["tweet_id"] = entry['id']
				# media_list.append(item)
				yield item
			# return media_list
		else:
			return

	def get_place(self,main=True):
		if main:
			if "retweeted_status" in self.tweet_dict:
				entry = self.tweet_dict['retweeted_status']
			elif "quoted_status" in self.tweet_dict:
				entry = self.tweet_dict['quoted_status']
			else:
				entry = self.tweet_dict
		else:
			entry = self.tweet_dict
		place = entry['place']
		if place != None:
			try:
				del place["id"]
				del place["contained_within"]
				del place["attributes"]
				# if place['coordinates'] is not None:
				place['coordinates'] = str(place["bounding_box"]["coordinates"])
				del place["bounding_box"]
			except KeyError:
				pass
			except TypeError: #place['coordinates'] is null
				place['coordinates'] = None
			finally:
				place["tweet_id"] = entry['id']
			return place
		else:
			return

if __name__ == '__main__':
	#tweet example
	import pymongo
	from bson.objectid import ObjectId
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["twitter_new"]
	collection = db["tweet"]
	
	"""
	#get status with retweet
	query_result1 = collection.find({"_id":ObjectId("5e54abe0804d49fb9afea7c1")})
	tweet1 = next(query_result1)
	#get main tweet (retweeted tweet)
	data1 = TweetDataExtractor(tweet1['tweet_object'])
	main1 = data1.get_main_tweet()
	#get retweet data
	rt = data1.get_rt_data()
	user1 = data1.get_user()
	user_mentions1 = data1.get_mention_user()	
	"""

	"""
	#get status with quote
	query_result2 = collection.find({"_id":ObjectId("5e54abe0804d49fb9afea7be")})
	tweet2 = next(query_result2)
	#get main tweet (quoted tweet)
	data2 = TweetDataExtractor(tweet2['tweet_object'])
	main2 = data2.get_main_tweet()
	#get quote data
	qt = data2.get_quote_data()
	user2 = data2.get_user()
	user_mentions2 = data2.get_mention_user()
	"""	
	
	"""
	#place
	place_tweet = collection.find({"_id":ObjectId("5e54abe0804d49fb9afea7f8")})
	tweet_place = next(place_tweet)
	data_place = TweetDataExtractor(tweet_place['tweet_object'])
	place3 = data_place.get_place() 
	"""

	
	#hashtags
	ht_tweet = collection.find({"_id":ObjectId("5e54abe0804d49fb9afea7bf")})
	tweet_ht = next(ht_tweet)
	data_ht = TweetDataExtractor(tweet_ht['tweet_object'])
	hashtags = data_ht.get_hashtags()


	"""
	# media
	media_tweet = collection.find({"_id":ObjectId("5e54d803c73f53a03398db86")})
	tweet_media = next(media_tweet)
	data_media = TweetDataExtractor(tweet_media['tweet_object'])
	media = data_media.get_media()
	"""

	"""
	# symbols
	sym_tweet = collection.find({"_id":ObjectId("5e54d7b4c73f53a03398cca1")})
	tweet_sym = next(sym_tweet)
	data_sym = TweetDataExtractor(tweet_sym['tweet_object'])
	symbols = data_sym.get_symbol()
	"""