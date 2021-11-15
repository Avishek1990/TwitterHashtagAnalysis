import CryptoTweetsSentiment as cts

cryptoTweets = cts.getTweets()
cryptoTweets.enterSearchCriteria('Bitcoin',"2021-11-13","2021-11-14")
tweets_Crypto = cryptoTweets.searchTweets()

