import os
#TOKEN de prod
token = os.environ.get('FB_ACCESS_TOKEN')
FB_VERIFY_TOKEN = (os.environ.get('FB_VERIFY_TOKEN'))
#if token==None:
    #TOKEN de test
 #   token="EAAFo1IiXrQwBABjWTFk7ZA4XL2kmhFt6M0t0pTjJWSGRppsTWQOYI7Lylcub4899ZBpZBOHz3N4CfvABclqw7ZA5CNZB1JtfhtFEVShC8KP3ZB3GLqmc5RLtnBX3WGl1aMM0zYvm6DAxIvCeOXem1YsFqpcVsrp1pZAzpkeF0QeCAZDZD"

#if FB_VERIFY_TOKEN==None:
#    FB_VERIFY_TOKEN = "test_token"

me = os.environ.get('MY_ID')