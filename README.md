![Nraj3Rf.jpg](https://bitbucket.org/repo/jqrp9G/images/3208140985-Nraj3Rf.jpg)

# README #

This is a simple sentiment analyzing Twitter bot that keeps track of Donald Trump (@realdonaldtrump)'s emotional state. Based on the tweets observed in 10 minute window, the bot will tweet an appropriately severe warning (ranging from all clear to [PINNACLE NUCFLASH](https://en.wikipedia.org/wiki/United_States_military_nuclear_incident_terminology)) to notify followers of potentially important current events. It includes a manually labeled training corpus of his tweets into three categories: positive, neutral, and negative.

### What is this repository for? ###

Pure fun, and possibly to give enough warning to reach a fallout shelter if needed. You may also want to look at [Trump2cash](https://github.com/maxbbraun/trump2cash) in case you are interested in using sentiment analysis of Trump to buy and sell stocks. Since this is a mini-project to teach myself basic natural language processing, I don't intend to extend the functionality much, but I may expand the training corpus as Trump tweets more.

### How do I get set up? ###

You can clone the repository immediately assuming you have the following packages installed:

* NLTK (natural language toolkit)
* python-twitter
* psycopg2
* Postgres

You will need to include an api.key file that contains your [Twitter](apps.twitter.com) tokens, plus a db.key file that contains your database access credentials as well.

### Who do I talk to? ###

Please feel free to contact [me](mailto:james.winkler@gmail.com) with questions or comments.