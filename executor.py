import CryptoTweetsSentiment as cts

cryptoTweets = cts.getTweets()
cryptoTweets.enterSearchCriteria('Bitcoin',"2021-11-14","2021-11-15")
tweets_Crypto = cryptoTweets.searchTweets()

