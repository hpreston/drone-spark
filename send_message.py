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

def get_roomId(destination):
    '''
    Determine the roomId to send the message to.
    '''

    # If an explict roomId was provided as a varg, verify it's a valid roomId
    # if ("roomId" in destination.keys()):
    if (destination["roomId"]):
        if verify_roomId(destination["roomId"]):
            return destination["roomId"]
    # If a roomName is provided, send to room with that title
    # elif ("roomName" in destination.keys()):
    elif (destination["roomName"]):
        # Try to find room based on room name
        response = requests.get(
            spark_urls["rooms"],
            headers = spark_headers
        )
        rooms = response.json()["items"]
        #print("Number Rooms: " + str(len(rooms)))
        for room in rooms:
            #print("Room: " + room["title"])
            if destination["roomName"] == room["title"]:
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

def standard_message(build_info):
    '''
    This will create a standard notification message.
    '''
    status = build_info["build_status"]
    repo = "{}/{}".format(build_info["repo_owner"], build_info["repo_name"])
    if status == "success":
        message = "##Build for %s is Successful \n" % (repo)
        message = message + "**Build author:** %s <%s> \n" % (build_info["commit_author"],build_info["commit_author_email"])
    else:
        message = "#Build for %s FAILED!!! \n" % (repo)
        message = message + "**Drone blames build author:** %s <%s> \n" % (build_info["commit_author"],build_info["commit_author_email"])

    message = message + "###Build Details \n"
    message = message + "* [Build Log](%s)\n" % (build_info["build_link"])
    message = message + "* [Commit Log](%s)\n" % (build_info["commit_log"])
    message = message + "* **Branch:** %s\n" % (build_info["commit_branch"])
    message = message + "* **Event:** %s\n" % (build_info["build_event"])
    message = message + "* **Commit Message:** %s\n" % (build_info["commit_message"])

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
    # payload = drone.plugin.get_input()
    # vargs = payload["vargs"]

    # Retrieve Plugin Parameters
    # auth_token = os.getenv("AUTH_TOKEN")
    auth_token = os.getenv("SPARK_TOKEN")
    destination = {
                    "roomName": os.getenv("PLUGIN_ROOMNAME"),
                    "roomId": os.getenv("PLUGIN_ROOMID"),
                    "personEmail": os.getenv("PLUGIN_PERSONEMAIL")
                  }
    message = os.getenv("PLUGIN_MESSAGE")

    build_info = {
                    "repo_owner": os.getenv("DRONE_REPO_OWNER"),
                    "repo_name": os.getenv("DRONE_REPO_NAME"),
                    "commit_sha": os.getenv("DRONE_COMMIT_SHA"),
                    "commit_ref": os.getenv("DRONE_COMMIT_REF"),
                    "commit_branch": os.getenv("DRONE_COMMIT_BRANCH"),
                    "commit_author": os.getenv("DRONE_COMMIT_AUTHOR"),
                    "commit_author_email": os.getenv("DRONE_COMMIT_AUTHOR_EMAIL"),
                    "build_event": os.getenv("DRONE_BUILD_EVENT"),
                    "build_number": os.getenv("DRONE_BUILD_NUMBER"),
                    "build_status": os.getenv("DRONE_BUILD_STATUS"),
                    "build_link": os.getenv("DRONE_BUILD_LINK"),
                    "build_started": os.getenv("DRONE_BUILD_STARTED"),
                    "build_created": os.getenv("DRONE_BUILD_CREATED"),
                    "tag": os.getenv("DRONE_TAG"),
                    "job_started": os.getenv("DRONE_JOB_STARTED"),
                    "commit_message": os.getenv("CI_COMMIT_MESSAGE"),
                    "commit_log": os.getenv("CI_BUILD_LINK")
                }

    # Debug Info
    # print("destination details:")
    # print(destination)
    # print("build_info details: ")
    # print(build_info)
    # print(" ")



    # Prepare headers and message objects
    spark_headers["Authorization"] = "Bearer %s" % (auth_token)
    spark_message = {}

    # Determine destination for message
    try:
        # First look for a valid roomId or roomName
        roomId = get_roomId(destination)
        # Debug
        # print("roomId = {}".format(roomId))
        spark_message["roomId"] = roomId
    except LookupError:
        # See if a personEmail was provided
        # if "personEmail" in destination.keys():
        if destination["personEmail"]:
            spark_message["toPersonEmail"] = destination["personEmail"]
        else:
            raise(LookupError("Requires valid roomId, roomName, or personEmail to be provided.  "))

    # Send Standard message
    standard_notify = send_message(spark_message, standard_message(build_info))
    if standard_notify.status_code != 200:
        print(standard_notify)
        raise(SystemExit("Something went wrong..."))

    # If there was a message sent from .drone.yml
    # if "message" in vargs.keys():
    if message:
        custom_notify = send_message(spark_message, message)
        if custom_notify.status_code != 200:
            print(custom_notify.text)
            raise (SystemExit("Something went wrong..."))



if __name__ == "__main__":
    # Debug
    # print(os.environ)

    main()
