#!/usr/bin/env python
'''
This is the Python Code for a drone.io plugin to send messages using Cisco Spark
'''

import drone
import requests
import os

spark_urls = {
    "messages": "https://api.ciscospark.com/v1/messages",
    "rooms": "https://api.ciscospark.com/v1/rooms",
    "people": "https://api.ciscospark.com/v1/people"
}

spark_headers = {}
spark_headers["Content-type"] = "application/json"

def get_roomId(payload):
    '''
    Determine the roomId to send the message to.
    '''

    # If an explict roomId was provided as a varg, verify it's a valid roomId
    if ("roomId" in payload["vargs"].keys()):
        if verify_roomId(payload["vargs"]["roomId"]):
            return payload["vargs"]["roomId"]
    # If a roomName is provided, send to room with that title
    elif ("roomName" in payload["vargs"].keys()):
        # Try to find room based on room name
        response = requests.get(
            spark_urls["rooms"],
            headers = spark_headers
        )
        rooms = response.json()["items"]
        # print("Number Rooms: " + str(len(rooms)))
        for room in rooms:
            # print("Room: " + room["title"])
            if payload["vargs"]["roomName"] == room["title"]:
                return room["id"]

    # If no valid roomId could be found in the payload, raise error
    raise(LookupError("roomId can't be determined"))

def verify_roomId(roomId):
    '''
    Check if the roomId provided is valid
    '''
    url = "%s/%s" % (spark_urls["rooms"], roomId)

    response = requests.get(
        url,
        headers = spark_headers
    )

    if response.status_code == 200:
        return True
    else:
        return False

def standard_message(payload):
    '''
    This will create a standard notification message.
    '''
    status = payload["build"]["status"]
    if status == "success":
        message = "##Build for %s is Successful \n" % (payload["repo"]["full_name"])
        message = message + "Build author: [%s](%s) \n" % (payload["build"]["author"], payload["build"]["author_email"])
    else:
        message = "#Build for %s FAILED!!!" % (payload["repo"]["full_name"])
        message = message + "Drone blames build author: [%s](%s) \n" % (payload["build"]["author"], payload["build"]["author_email"])

    message = message + "###Build Details \n"
    message = message + "* [Build Log](%s/%s/%s)\n" % (payload["system"]["link_url"], payload["repo"]["full_name"], payload["build"]["number"])
    message = message + "* [Commit Log](%s)\n" % (payload["build"]["link_url"])
    message = message + "* **Branch:** %s\n" % (payload["build"]["branch"])
    message = message + "* **Commit Message:** %s\n" % (payload["build"]["message"])

    return message

def send_message(message_data, message_text):

    message_data["markdown"] = message_text

    response = requests.post(
        spark_urls["messages"],
        headers = spark_headers,
        json = message_data
    )

    return response

def main():
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    # Prepare headers and message objects
    spark_headers["Authorization"] = "Bearer %s" % (vargs["auth_token"])
    spark_message = {}

    # Determine destination for message
    try:
        # First look for a valid roomId or roomName
        roomId = get_roomId(payload)
        spark_message["roomId"] = roomId
    except LookupError:
        # See if a personEmail was provided
        if "personEmail" in vargs.keys():
            spark_message["toPersonEmail"] = vargs["personEmail"]
        else:
            raise(LookupError("Requires valid roomId, roomName, or personEmail to be provided.  "))

    # Send Standard message
    standard_notify = send_message(spark_message, standard_message(payload))
    if standard_notify.status_code != 200:
        print(standard_notify.json()["message"])
        raise(SystemExit("Something went wrong..."))

    # If there was a message sent from .drone.yml
    if "message" in vargs.keys():
        custom_notify = send_message(spark_message, vargs["message"])
        if custom_notify.status_code != 200:
            print(custom_notify.json()["message"])
            raise (SystemExit("Something went wrong..."))



if __name__ == "__main__":
    main()