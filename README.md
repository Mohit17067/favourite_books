# Favourite_Books
A Docker container with a rest api made on a flask application. The application contains favourite_books of a user with
fields - `title, amazon_url, author, genre`. Authentication is handled with JSON Web Tokens.

## Installation & Setup
  * Clone the repository - `"git clone https://github.com/Mohit17067/favourite_books"`
  * In the directory, run - `"docker-compose build"`. This will build the container with all the requirements.
  * After building, run - `"docker-compose run --rm api flask db upgrade"`
  * To run the application in the container - `"docker-compose up api"`. <br>
  **Note: Keep this instance of the terminal running. Open a new terminal.**

## Authentication of a client
  * **We need to create a new client in the shell to generate the jwt token**.<br> 
    Run - `"docker-compose run api flask shell"`
  * In the flask shell, run the following commands:
    * Import Modules --- `"from favourite_books.models import db, Client"`
    * Create Client  --- `"cl = Client(name="Demo Client")"`
    * Add Client to db  ---  `"db.session.add(cl)"`
    * Commit to db  ---   `"db.session.commit()"`
  * In the shell, run `"(cl.client_id, str(cl.secret_key))"` to view the details of the client created.<br>
    Details: **client_id** = `59J43SaNa6GPTtEoiRtYaV` & **client_secret** = `ca3dd71a-a4a2-4647-9c1b-650a42d167aa`.
    **Note: These details could be used direclty as the client already exists in the database.**
 
 
<br>
<br>

### The `client_id` is used as an `api_key` to access the service.
### The client details are used to generate the jwt token.
<br>
<br>

## JWT Token Generation
**API Users could generate the token using [libraries](https://jwt.io/#libraries) for their language**.<br>

**client_id**(generated above) is used in the payload to generate the jwt token.<br>
Other features of the payload can be seen in the `encode_client_token` function in [utils.py](https://github.com/Mohit17067/favourite_books/blob/master/favourite_books/apis/v1/utils.py#L39).<br>
    
    def encode_client_token(client, user_id=None):
      iat = datetime.utcnow()
      exp = iat + timedelta(hours=2)
      nbf = iat
      payload = {
          'exp': exp,
          'iat': iat,
          'nbf': nbf,
          'aud': str(client.id)
      }
      if user_id:
          payload['sub'] = user_id

      return jwt.encode(
          payload,
          str(client.secret_key),
          algorithm='HS256',
          headers=None
      ).decode('utf-8')
      
## To generate the token using the above funtion, 
  * Enter flask shell - `"docker-compose run api flask shell"`
  * In the flask shell, run the following commands:
    * Import Modules --- `"from favourite_books.models import Client"` &<br> "`from favourite_books.apis.v1.utils import encode_client_token`"
    * Get Client  --- `"cl = Client.query.get(3)"`
    * Call Function  ---  ```encode_client_token(cl)```. <br>JWT Token in returned:
    `'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2ODI5OTQsImlhdCI6MTU4NjY4MTE5NCwibmJmIjoxNTg2NjgxMTk0LCJhdWQiOiIzIn0.tLhi-Hk84BnsJVJDVCLrKVfl3RdnpbmMLQ8BEEasZtg'`
    
    **Note: The Token expires in 2 hours as passed in the `exp` field of the payload.**
 <br><br>   

## CRUD Operations in the API
To access the api,<br>
```
curl -H "Authorization: Bearer <YOUR_TOKEN>" localhost:8080/v1/books?api_key=<YOUR_CLIENT_ID> | python3 -m json.tool
```

### Create Operation -
**New Book**
```
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2OTkwMzUsImlhdCI6MTU4NjY5MTgzNSwibmJmIjoxNTg2NjkxODM1LCJhdWQiOiIzIn0.SYvXhAT7anNvgrjJ0ZgzAJ_CVQJzuXrnEvR1njy3zw0" -H "Content-Type: application/json" -d '{"title": "City of Girls: A Novel", "amazon_url": "https://www.amazon.com/dp/1594634734/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=6A8890MVC9YR032WA0AS&pf_rd_t=101&pf_rd_p=2c410138-b3ec-461a-8052-6765deddd3eb&pf_rd_i=7031012011", "author": "Elizabeth Gilbert", "genre": "Historical Fiction"}' -X POST localhost:8080/v1/books?api_key=59J43SaNa6GPTtEoiRtYaV | python3 -m json.tool
```
**Result** -
```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   780  100   445  100   335  11125   8375 --:--:-- --:--:-- --:--:-- 19500
{
    "payload": {
        "id": 4,
        "created_at": "2020-04-12T11:49:01.347928",
        "updated_at": "2020-04-12T11:49:01.347938",
        "title": "City of Girls: A Novel",
        "amazon_url": "https://www.amazon.com/dp/1594634734/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=6A8890MVC9YR032WA0AS&pf_rd_t=101&pf_rd_p=2c410138-b3ec-461a-8052-6765deddd3eb&pf_rd_i=7031012011",
        "author": "Elizabeth Gilbert",
        "genre": "Historical Fiction"
    }
}
```

### Read Operation-
**Read all books**-
  ```
  curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2OTkwMzUsImlhdCI6MTU4NjY5MTgzNSwibmJmIjoxNTg2NjkxODM1LCJhdWQiOiIzIn0.SYvXhAT7anNvgrjJ0ZgzAJ_CVQJzuXrnEvR1njy3zw0" localhost:8080/v1/books?api_key=59J43SaNa6GPTtEoiRtYaV | python3 -m json.tool
  ```
**Result**
```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1129  100  1129    0     0   137k      0 --:--:-- --:--:-- --:--:--  137k
{
    "payload": [
        {
            "id": 2,
            "created_at": "2020-04-11T16:53:34.031453",
            "updated_at": "2020-04-11T16:53:34.031461",
            "title": "Then She Was Gone: A Novel",
            "amazon_url": "https://www.amazon.com/Then-She-Was-Gone-Novel/dp/B07BQFXLFN/ref=sr_1_2?dchild=1&keywords=fiction+books&qid=1586623754&s=books&sr=1-2",
            "author": "Lisa Jewell",
            "genre": "Crime Fiction"
        },
        {
            "id": 3,
            "created_at": "2020-04-11T17:00:23.556777",
            "updated_at": "2020-04-11T17:00:23.556782",
            "title": "The Hideaway",
            "amazon_url": "https://www.amazon.com/Hideaway-Lauren-K-Denton-ebook/dp/B01HAK33TC/ref=sr_1_3?dchild=1&keywords=fiction+books&qid=1586624043&s=books&sr=1-3",
            "author": "Lauren K. Denton",
            "genre": "Christian Fiction"
        },
        {
            "id": 4,
            "created_at": "2020-04-12T11:49:01.347928",
            "updated_at": "2020-04-12T11:49:01.347938",
            "title": "City of Girls: A Novel",
            "amazon_url": "https://www.amazon.com/dp/1594634734/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=6A8890MVC9YR032WA0AS&pf_rd_t=101&pf_rd_p=2c410138-b3ec-461a-8052-6765deddd3eb&pf_rd_i=7031012011",
            "author": "Elizabeth Gilbert",
            "genre": "Historical Fiction"
        }
    ]
}
```

**Read book with id 2**
```
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2OTkwMzUsImlhdCI6MTU4NjY5MTgzNSwibmJmIjoxNTg2NjkxODM1LCJhdWQiOiIzIn0.SYvXhAT7anNvgrjJ0ZgzAJ_CVQJzuXrnEvR1njy3zw0" localhost:8080/v1/books/2?api_key=59J43SaNa6GPTtEoiRtYaV | python3 -m json.tool
```
**Result**
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   351  100   351    0     0  43875      0 --:--:-- --:--:-- --:--:-- 43875
{
    "payload": {
        "id": 2,
        "created_at": "2020-04-11T16:53:34.031453",
        "updated_at": "2020-04-11T16:53:34.031461",
        "title": "Then She Was Gone: A Novel",
        "amazon_url": "https://www.amazon.com/Then-She-Was-Gone-Novel/dp/B07BQFXLFN/ref=sr_1_2?dchild=1&keywords=fiction+books&qid=1586623754&s=books&sr=1-2",
        "author": "Lisa Jewell",
        "genre": "Crime Fiction"
    }
}
```

### Update Operation -
**Update Genre of Book with id 2 (Crime Fiction - Historical Fiction)**
```
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2OTkwMzUsImlhdCI6MTU4NjY5MTgzNSwibmJmIjoxNTg2NjkxODM1LCJhdWQiOiIzIn0.SYvXhAT7anNvgrjJ0ZgzAJ_CVQJzuXrnEvR1njy3zw0" -H  "Content-Type: application/json" -d '{"id": 2, "genre":"Historical Fiction", "title": "Then She Was Gone: A Novel", "amazon_url": "https://www.amazon.com/Then-She-Was-Gone-Novel/dp/B07BQFXLFN/ref=sr_1_2?dchild=1&keywords=fiction+books&qid=1586623754&s=books&sr=1-2", "author": "Lisa Jewell"}' -X PUT localhost:8080/v1/books/2?api_key=59J43SaNa6GPTtEoiRtYaV | python3 -m json.tool
```
**Result**
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   610  100   356  100   254  16181  11545 --:--:-- --:--:-- --:--:-- 27727
{
    "payload": {
        "id": 2,
        "created_at": "2020-04-11T16:53:34.031453",
        "updated_at": "2020-04-11T16:53:34.031461",
        "title": "Then She Was Gone: A Novel",
        "amazon_url": "https://www.amazon.com/Then-She-Was-Gone-Novel/dp/B07BQFXLFN/ref=sr_1_2?dchild=1&keywords=fiction+books&qid=1586623754&s=books&sr=1-2",
        "author": "Lisa Jewell",
        "genre": "Historical Fiction"
    }
}
```

### Delete Operation -
**Delete book with id 4**
```
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY2OTkwMzUsImlhdCI6MTU4NjY5MTgzNSwibmJmIjoxNTg2NjkxODM1LCJhdWQiOiIzIn0.SYvXhAT7anNvgrjJ0ZgzAJ_CVQJzuXrnEvR1njy3zw0" -X DELETE localhost:8080/v1/books/4?api_key=59J43SaNa6GPTtEoiRtYaV | python3 -m json.tool
```
**Result of reading all books after deleting**
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   700  100   700    0     0  58333      0 --:--:-- --:--:-- --:--:-- 58333
{
    "payload": [
        {
            "id": 2,
            "created_at": "2020-04-11T16:53:34.031453",
            "updated_at": "2020-04-11T16:53:34.031461",
            "title": "Then She Was Gone: A Novel",
            "amazon_url": "https://www.amazon.com/Then-She-Was-Gone-Novel/dp/B07BQFXLFN/ref=sr_1_2?dchild=1&keywords=fiction+books&qid=1586623754&s=books&sr=1-2",
            "author": "Lisa Jewell",
            "genre": "Historical Fiction"
        },
        {
            "id": 3,
            "created_at": "2020-04-11T17:00:23.556777",
            "updated_at": "2020-04-11T17:00:23.556782",
            "title": "The Hideaway",
            "amazon_url": "https://www.amazon.com/Hideaway-Lauren-K-Denton-ebook/dp/B01HAK33TC/ref=sr_1_3?dchild=1&keywords=fiction+books&qid=1586624043&s=books&sr=1-3",
            "author": "Lauren K. Denton",
            "genre": "Christian Fiction"
        }
    ]
}
```

## Token Expiration
**As specified in the payload, the token expires in 2 hours.<br>
After expiration, an exception is generated to re-authenicate with new token.**

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    52  100    52    0     0   5777      0 --:--:-- --:--:-- --:--:--  5777
{
    "message": "Token Expired. Please Re-Authenticate"
}
```

### References
  * [Medium Tutorial on building Rest API](https://medium.com/python-rest-api-toolkit/build-a-python-rest-api-in-5-minutes-c183c00d3465)
  * [Medium Tutorial of using JWT Tokens](https://medium.com/python-rest-api-toolkit/python-rest-api-authentication-with-json-web-tokens-1e06e449f33)
  * [Check Expiration of Token](https://www.programcreek.com/python/example/105944/jwt.ExpiredSignatureError)
  
