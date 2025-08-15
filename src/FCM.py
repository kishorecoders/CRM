from fastapi import  HTTPException
from pydantic import BaseModel
import time
import jwt
import requests
import json
from fastapi import APIRouter

router = APIRouter()


def _get_access_token():

    service_account_email = "firebase-adminsdk-fbsvc@wings-fa3f5.iam.gserviceaccount.com"
    private_key = """-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPFmY87ztOepOi\njiGHvfMwkgO5m0YrlSOMdEBvAcJO0zZH/UG5JKw4vA7u5hO22pCd8gPzof6pJbTw\nSVPL3fMg65VnadGixWq/n9JIskCX2IUG/3fNq03vDJOLnt1xKEVMQ1681lD319AE\nUzatMq0R2o4Q1uABpUp6CuJt5wkylfFEQk8Y5zOED30tLAyXw7NLp92vuWlqgBuS\nxeExwzV3BgOGfriJOoMSgTtJYiROti/8HQl8S+f2tK1p0CAzo4XBilb6T+v4e4Iv\n/3pTlrr5w2BpddzYvXZT0s0Lg456PdwnkcroWCu+Oslevz9IMI0zFG8m0flwQzk6\nxx6++A/DAgMBAAECggEAJh07R+/H/JO25G5AYZlmTwQwx1J6wb67QjiLO2MZfiSF\nkw5bsFW9lNuX7ARQkJD9mPRYIdko47za5na4g4cgHmj9oIDrYofvM8GYlGSqWsgx\nA661QBdNSrgH1+SvYQpGZtjncN4JHPSNhp5CK/JtxCFzkEncBLGFWZzzO8MQAE0f\nV7MbOZqjHiYIkmk6mHYebFVdCuwAP6NrCPObrYK7UFtHTBFMZl1N27YcL3TS8rej\n63ucwnnIfGkbiSQnRmcaIJ68I2/N5GJ2OT6aEBFDILnWNIOa9Bmfc5v1eug8XrhG\nzu97/Lo7T4VybrJ0sWovqjCW66HzHIiqQR+YGUbKYQKBgQD/u4eK2/rtWF78BhAu\nsHJKOcaBQZWwz3EPPO0tUwNArpRxmD1NxNLw8j2HNJzqV3zAfUxCws/BibVbTbKw\nt2Eipu8Xlq7uHWsFgxGuWh1pNuYmmNtAXZChpGKKwexrPhmnm+5bHW8fgT8dKDbi\n5yVsu05HqZOlCg6RnQUFaZ47qwKBgQDPTdh1x7qNjOl0HKvI0Fa9chIPuMhDwXsP\n+lvaAazhO+4pDqFWkcVqzFjCcALEOftHcZT2edhIbAeZX6fDOOMqnMYwMHskkE6d\n9eDdcthgR0eJZW2ruduNusjSzWU8IZkdg2W9uLIewCEcvObyTk42kzCL1H8sZ1Bm\nCiEntF8kSQKBgQDsg8AECRe103lllSX6SG4rf+u7N7D96Z0i/rJMrO3hMJVRyf9I\nobSF60REe8B0a52RWVDindIPqRD19JJDJhbMOZ//LPl0d/i3DFWZ7vYsjP2mzNBa\nYy6UkLgipN/G/5Qyk+CKnFpdxOdeTAcXK7hNK55mYMuQZBC9U3+FVf1mKQKBgEE1\nZHyQCg+SnrDGgAbX+iD3a9UENAKULui0wQXPdxkWZ/EESB3aFrZkdxsabtRYxMER\namEprK4DRVSqcTQIhfSWggUQivvSZNhtSoF+KbAHW+pNPHVDLlvjwF4G++wxSV+u\nQGewXF8t4nyOszrPBO1H2YJyolpOWUzvrMQ3iaH5AoGAEc7r9wTQeN96fBjPtDQS\neS4aFqudpUGN6SCXWWgM+IyUqak4RQ8dAZBfHMybxsRCImMmvMAmX2vfOCnNHUdy\nxrB1T9mmxNrG293bUmlkC2Obl7pBx/UZGXj853we0PQkwvujPZIdWHa7nQ7uIJVP\nPBoYZxVvWdq5uHwW3Be98ZA=\n-----END PRIVATE KEY-----\n""".replace('\\n', '\n')  

    payload = {
        'iss': service_account_email,
        'sub': service_account_email,
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600,
        'scope': 'https://www.googleapis.com/auth/firebase.messaging'
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    response = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': encoded_jwt
    })

    if response.status_code == 200:
        oauth2_token = response.json()['access_token']
        return oauth2_token
    else:
        print("Error Fetching Token:", response.text)
        return None



def sendPush(msg, token, title, data):
    url = "https://fcm.googleapis.com/v1/projects/wings-fa3f5/messages:send"

    payload = json.dumps({
        "message": {
            "token": token,
            "data": data,
            "notification": {
                "title": title,
                "body": msg
            },
            "apns": {
                "payload": {
                    "aps": {
                        "sound": "default"
                    }
                }
            }
        }
    })

    access_token = _get_access_token()
    if not access_token:
        print("Failed to get access token.")
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        print(" Push Notification Sent Successfully!")
    else:
        print("Push Notification Failed:", response.text)

    return response


#############################################################################################################################################

service_account_email = "firebase-adminsdk-fbsvc@wings-fa3f5.iam.gserviceaccount.com"
private_key = """-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPFmY87ztOepOi\njiGHvfMwkgO5m0YrlSOMdEBvAcJO0zZH/UG5JKw4vA7u5hO22pCd8gPzof6pJbTw\nSVPL3fMg65VnadGixWq/n9JIskCX2IUG/3fNq03vDJOLnt1xKEVMQ1681lD319AE\nUzatMq0R2o4Q1uABpUp6CuJt5wkylfFEQk8Y5zOED30tLAyXw7NLp92vuWlqgBuS\nxeExwzV3BgOGfriJOoMSgTtJYiROti/8HQl8S+f2tK1p0CAzo4XBilb6T+v4e4Iv\n/3pTlrr5w2BpddzYvXZT0s0Lg456PdwnkcroWCu+Oslevz9IMI0zFG8m0flwQzk6\nxx6++A/DAgMBAAECggEAJh07R+/H/JO25G5AYZlmTwQwx1J6wb67QjiLO2MZfiSF\nkw5bsFW9lNuX7ARQkJD9mPRYIdko47za5na4g4cgHmj9oIDrYofvM8GYlGSqWsgx\nA661QBdNSrgH1+SvYQpGZtjncN4JHPSNhp5CK/JtxCFzkEncBLGFWZzzO8MQAE0f\nV7MbOZqjHiYIkmk6mHYebFVdCuwAP6NrCPObrYK7UFtHTBFMZl1N27YcL3TS8rej\n63ucwnnIfGkbiSQnRmcaIJ68I2/N5GJ2OT6aEBFDILnWNIOa9Bmfc5v1eug8XrhG\nzu97/Lo7T4VybrJ0sWovqjCW66HzHIiqQR+YGUbKYQKBgQD/u4eK2/rtWF78BhAu\nsHJKOcaBQZWwz3EPPO0tUwNArpRxmD1NxNLw8j2HNJzqV3zAfUxCws/BibVbTbKw\nt2Eipu8Xlq7uHWsFgxGuWh1pNuYmmNtAXZChpGKKwexrPhmnm+5bHW8fgT8dKDbi\n5yVsu05HqZOlCg6RnQUFaZ47qwKBgQDPTdh1x7qNjOl0HKvI0Fa9chIPuMhDwXsP\n+lvaAazhO+4pDqFWkcVqzFjCcALEOftHcZT2edhIbAeZX6fDOOMqnMYwMHskkE6d\n9eDdcthgR0eJZW2ruduNusjSzWU8IZkdg2W9uLIewCEcvObyTk42kzCL1H8sZ1Bm\nCiEntF8kSQKBgQDsg8AECRe103lllSX6SG4rf+u7N7D96Z0i/rJMrO3hMJVRyf9I\nobSF60REe8B0a52RWVDindIPqRD19JJDJhbMOZ//LPl0d/i3DFWZ7vYsjP2mzNBa\nYy6UkLgipN/G/5Qyk+CKnFpdxOdeTAcXK7hNK55mYMuQZBC9U3+FVf1mKQKBgEE1\nZHyQCg+SnrDGgAbX+iD3a9UENAKULui0wQXPdxkWZ/EESB3aFrZkdxsabtRYxMER\namEprK4DRVSqcTQIhfSWggUQivvSZNhtSoF+KbAHW+pNPHVDLlvjwF4G++wxSV+u\nQGewXF8t4nyOszrPBO1H2YJyolpOWUzvrMQ3iaH5AoGAEc7r9wTQeN96fBjPtDQS\neS4aFqudpUGN6SCXWWgM+IyUqak4RQ8dAZBfHMybxsRCImMmvMAmX2vfOCnNHUdy\nxrB1T9mmxNrG293bUmlkC2Obl7pBx/UZGXj853we0PQkwvujPZIdWHa7nQ7uIJVP\nPBoYZxVvWdq5uHwW3Be98ZA=\n-----END PRIVATE KEY-----\n""".replace('\\n', '\n')  


def _get_access_token2():
    payload = {
        'iss': service_account_email,
        'sub': service_account_email,
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600,
        'scope': 'https://www.googleapis.com/auth/firebase.messaging'
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    response = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': encoded_jwt
    })

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Error Fetching Token:", response.text)
        return None


class PushRequest(BaseModel):
    msg: str
    token: str
    title: str
    data: dict


@router.post("/send-push/")
def send_push_notification(payload: PushRequest):
    url = "https://fcm.googleapis.com/v1/projects/wings-fa3f5/messages:send"

    body = json.dumps({
        "message": {
            "token": payload.token,
            "data": payload.data,
            "notification": {
                "title": payload.title,
                "body": payload.msg
            },
            "apns": {
                "payload": {
                    "aps": {
                        "sound": "default"
                    }
                }
            }
        }
    })

    access_token = _get_access_token2()
    if not access_token:
        raise HTTPException(status_code=500, detail="Failed to get Firebase access token")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        return {"status": "success", "message": "Push notification sent"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
