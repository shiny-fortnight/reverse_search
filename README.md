# Reverse Search
###Setup
``` shell
$ pip install flask
python reverseSearch.py
```
###Browser 
`http://localhost:5000`

###Resource
[PaulSec/osint-facebook-reset-password](https://github.com/PaulSec/osint-facebook-reset-password`)

##Setting/Retrieving API Keys
You will need the following API Keys:

1. White pages <[Register here](http://pro.whitepages.com/lp/search-by-api-signup/)>

2. Twitter <[Register an account here](https://apps.twitter.com/)>

3. OpenCNAM <[Register an account here](http://www.opencnam.com/register/)>

###Update the API keys in the config.py file
```
# White pages API Key
API_KEY

# Twitter API Keys
TWITTER_KEY
TWITTER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_STOKEN

# Open CNAM API Keys
OPEN_CNAM_KEY
OPEN_CNAM_SECRET
```

#How Twitter input search works

| Keyword Search Input        | Finds tweets....           |
| ------------- |:-------------:|
| watching now      | containing both “watching” and “now”. This is the default operator. |
| “happy hour”      | containing the exact phrase “happy hour”.      |
| scary,movie | tweets containing scary, tweets containing movie, tweets containing BOTH scary and movie     |
