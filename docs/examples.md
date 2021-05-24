# Examples

## POST a message
```bash
curl --location --request POST 'localhost:80/api/v1/send/sender-person/recipient-person' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'message=some stupidly long message that we store and stuff happens and things and stuff and things and stuff and things and things and stuff and stuff and things and stuff and things and stuff and things'
```

```bash
curl --location --request POST 'localhost:80/api/v1/send/tim/john' \
--form 'message="Hey. How are you?"'
```

## GET Messages
### GET Messages from All Users
* Get 100 messages in the last 30 days (or less if fewer messages available)
```bash
curl --location --request GET 'localhost:80/api/v1/query'
```
* Get an arbitrarily large number of messages since forever (really, since 1970, but no one used the backend in 1970)
```bash
curl --location --request GET 'localhost:80/api/v1/query?timestamp=0&count=999999999'
```
* Get messages sent after some timestamp (caps at 100 messages unless you specify a count, no pagination):
```bash
curl --location --request GET 'localhost:80/api/v1/query?timestamp=2021-05-24%2012:00:00%20GMT'
```
Also valid timestamps are epoch seconds (like `1621891550`) and datestamps (like `2021-05-24`).

#### GET Messages between Two Users
Same as above examples, except the usernames are inside the query path:
```bash
curl --location --request GET 'localhost:80/api/v1/query/tim/john'
```
Note that `/tim/john` and `/john/tim` will return the same results.
