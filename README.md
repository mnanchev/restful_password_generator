# One time secret, One time file share restful API

Restful API for sharing secrets and files with external organizations

The entire application is engineered using MVC architecture. The project
has the following structure:


    .
    ├── managers                   # Managers interact with DB models and external third party services
    ├── migrations                 # All migrations of the postgres database are stored here
    ├── mock_object                # Folder needed for the tests of external services like S3
    ├── models                     # Database table models
    ├── postman_collection         # Collection of the API endpoints
    ├── resources                  # Resources are the API endpoints
    ├── schemas                    # Schemas are used to validate the input of the API endpoints
    ├── services                   # Services are the external services used by the application     
    ├── tests                      # Tests are the unit and/or integration tests of the application 
    └── utils                      # Utils are the helper functions used by the application 


`main.py` starts the application.

`run-tests.sh` runs a simplistic test and generates the API
documentation below.

## Run the tests

    ./run-tests.sh

# REST API

The REST API to the example app is described below.

## Register a new user

### Request

`POST /register`

    curl --location --request POST 'http://127.0.0.1:5000/register' --header 'Content-Type: application/json' --data-raw '{"email": "example@example.com","password": "probkotestov123!"}'

### Response

    HTTP/1.1 201 Created
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Location: /login/1
    Content-Length: 36

    {"message": "Success", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjIyLCJleHAiOjE2NDEyMzUxMDMsInJvbGUiOiJDcmVhdG9yTW9kZWwifQ.bfnqQgfuHSz-AKAu8Vj3_vWcRlAy2TQwLgz3BoilSUk"}

![Register](./images/register.png)

## Register existing user and getting error

### Request

`POST /register`

    curl --location --request POST 'http://127.0.0.1:5000/register' --header 'Content-Type: application/json' --data-raw '{"email": "example@example.com","password": "probkotestov123!"}'

### Response

    HTTP/1.1 400 Bad request
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 400 Bad request
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {"message": "Duplicated key error"}

![Register Bad Request](./images/register_bad_request.png)

## Login

### Request

`POST /login`

    curl --location --request POST 'http://127.0.0.1:5000/login' 
         --header 'Content-Type: application/json' 
         --data-raw '{"email": "martin2759@gmail.com",
                      "password": "nanchev12!dsa3"
                      }'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Location: /login/1
    Content-Length: 36

    {
    "message": "Success",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE3LCJleHAiOjE2NDEyMzUxMTEsInJvbGUiOiJDcmVhdG9yTW9kZWwifQ.gYydyv2iVoGLWYL1335uvkeEt9yTeaGuvxNFCmP9teQ",
    "role": "signed_creator"
    }


![Login](./images/login.png)

## Generate Secret

### Request

`POST /generateSecret`

    curl --location --request POST 'http://127.0.0.1:5000/generateSecret' 
         --header 'Content-Type: application/json' 
         --header 'Authorization: Bearer eyJ0e' 
         --data-raw '{ "PasswordLength": 255,
                       "ExcludeCharacters": "",
                       "ExcludeNumbers": false,
                       "ExcludePunctuation":  true,
                       "ExcludeUppercase": true,
                       "ExcludeLowercase": true,
                       "IncludeSpace": false,
                       "secret":"hello world to the secret for the first time!",
                       "password":"probkotestov"
                    }'

- PasswordLength (integer) -- The length of the password. If you don't include this parameter, the default length is 32 characters.
- ExcludeCharacters (string) -- A string of the characters that you don't want in the password.
- ExcludeNumbers (boolean) -- Specifies whether to exclude numbers from the password. If you don't include this switch, the password can contain numbers.
- ExcludePunctuation (boolean) -- Specifies whether to exclude the following punctuation characters from the password: ! "" # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~ . If you don't include this switch, the password can contain punctuation.
- ExcludeUppercase (boolean) -- Specifies whether to exclude uppercase letters from the password. If you don't include this switch, the password can contain uppercase letters.
- ExcludeLowercase (boolean) -- Specifies whether to exclude lowercase letters from the password. If you don't include this switch, the password can contain lowercase letters.
- IncludeSpace (boolean) -- Specifies whether to include the space character. If you include this switch, the password can contain space characters.
- RequireEachIncludedType (boolean) -- Specifies whether to include at least one upper and lowercase letter, one number, and one punctuation. If you don't include this switch, the password contains at least one of every character type.
- secret (string) -- The secret to be used to generate the password, if the password is not generated from a secret manager, but provided by the user.
- password (string) -- The password to protect the shared secret.



### Response

    HTTP/1.1 201 Created
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Content-Length: 36

    {
    "message": "http://localhost:5000/getSecret/31c9831e-ab7e-4fd8-a9b6-c6c21260777a"
    }

## Get a secret

### Request

`GET /getSecret/<string:secret_id>`

    curl --location --request GET 'http://127.0.0.1:5000/getSecret/7c58ce7d-8c6b-4752-a997-11f6e5ec7b6a' 
    --header 'Content-Type: application/json' 
    --data-raw '{
        "password": "probkotestov"
    }'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {
    "message": "I am the secret you are looking for"
     }

![Get a secret](./images/get_secret.png)

## Get same secret again

### Request

`GET /getSecret/<string:secret_id>`

    curl --location --request GET 'http://127.0.0.1:5000/getSecret/7c58ce7d-8c6b-4752-a997-11f6e5ec7b6a' 
    --header 'Content-Type: application/json' 
    --data-raw '{
        "password": "probkotestov"
    }'

### Response

    HTTP/1.1 404 Not Found
    Date: Thu, 24 Feb 2011 12:36:31 GMT
    Status: 404 Not Found
    Connection: close
    Content-Type: application/json
    Location: /thing/2
    Content-Length: 35

    {
    "message": "Secret does not exist"
    }

![Get a secret one more time ](./images/get_secret_one_more_time.png)

## Change a secret

### Request

`PUT /putSecret/<string:secret_id>`

    curl --location --request PUT 'http://127.0.0.1:5000/putSecret/31c9831e-ab7e-4fd8-a9b6-c6c21260777a' 
    --header 'Content-Type: application/json' 
    --header 'Authorization: Bearer eyJ0e' 
    --data-raw '{
        "secret":"mnanchev",
        "password":"dskaljdlkaskd;askd;assdlcmx123"
    }'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:31 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 40

    {
    "message": "http://localhost:5000/getSecret/31c9831e-ab7e-4fd8-a9b6-c6c21260777a"
    }

![Change a secret](./images/change_a_secret.png)

## Attempt to change a Thing without required secret parameter

### Request

`PUT /putSecret/<string:secret_id>`

    curl --location --request PUT 'http://127.0.0.1:5000/putSecret/31c9831e-ab7e-4fd8-a9b6-c6c21260777a' 
    --header 'Content-Type: application/json' 
    --header 'Authorization: Bearer eyJ0e'  
    --data-raw '{}'



### Response

    HTTP/1.1 400 Bad Request
    Date: Thu, 24 Feb 2011 12:36:31 GMT
    Status: 400 Bad Request
    Connection: close
    Content-Type: application/json
    Content-Length: 40

    {
    "message": "{'secret': ['Missing data for required field.']}"
    }

![Change a secret without providing body](./images/change_a_secret_without_body.png)


## Delete a secret

### Request

`DELETE /deleteSecret/<string:secret_id>`

    curl --location --request DELETE 'http://127.0.0.1:5000/deleteSecret/b0fe447f-9a5f-4f2a-8741-39f374a3c08a' \
         --header 'Authorization: Bearer eyJ0eXAi'

### Response

    HTTP/1.1 204 No Content
    Date: Thu, 24 Feb 2011 12:36:32 GMT
    Status: 204 No Content
    Connection: close

Only the user, that creates the secret could delete it.
![Delete a secret](./images/delete.png)


## Try to delete same secret again

### Request

`DELETE /deleteSecret/<string:secret_id>`

    curl --location --request DELETE 'http://127.0.0.1:5000/deleteSecret/b0fe447f-9a5f-4f2a-8741-39f374a3c08a' \
         --header 'Authorization: Bearer eyJ0e'

### Response

    HTTP/1.1 404 Not Found
    Date: Thu, 24 Feb 2011 12:36:32 GMT
    Status: 404 Not Found
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {
    "message": "Secret does not exist"
    }

## Get deleted Thing

### Request

`GET /thing/1`

    curl --location --request GET 'http://127.0.0.1:5000/getSecret/b0fe447f-9a5f-4f2a-8741-39f374a3c08a' 
    --header 'Content-Type: application/json' 
    --data-raw '{
        "password": "probkotestov"
    }'

### Response

    HTTP/1.1 404 Not Found
    Date: Thu, 24 Feb 2011 12:36:33 GMT
    Status: 404 Not Found
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {
    "message": "Secret does not exist"
    }

![Get deleted secret](./images/get_deleted_secret.png)

## Upload a file and get pre-signed url for sharing with others

### Request

`POST /upload`

    curl --location --request POST 'http://127.0.0.1:5000/upload' \
        --header 'Authorization: Bearer eyJ0eXAi' \
        --form 'file=@"/Users/probkotestov/Downloads/Zoom.pkg"'

### Response

    HTTP/1.1 201 Created
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Location: /login/1
    Content-Length: 36

    {
    "message": "File uploaded successfully",
    "url": "SIGNED_URL_FOR_SHARING_WITH_THIRD_PARTIES"
    }


![File for sharing with others](./images/file_for_sharing-with_others.png)

## Get url, so third party organizations could upload files to S3

### Request
`Get /get_upload_url`

    curl --location --request GET 'http://127.0.0.1:5000/get_upload_url' \
         --header 'Authorization: EAy' \
         --header 'Content-Type: application/json' \
         --data-raw '{
            "object_name":"application",
            "expiration_time":7200
        }'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:31 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 40

    {
    "message": "Upload url generated successfully",
    "url": "https://secret_bucket.s3.amazonaws.com/f502eb0d-456e-40be-b2a1-79b76a36260b/application?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=""%2F20220101%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20220101T205932Z&X-Amz-Expires=7200&X-Amz-SignedHeaders=host&X-Amz-Signature=7ac3447fee85101158aa214b3730aad0774ff6cdc90c1887d62eec36d95ea274"
    }

![Get url for external organizations to upload files](./images/get_url_for_uploading_files.png)