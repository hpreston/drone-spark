# drone-spark

This is a plugin for [drone.io](http://drone.io), a Continuous Integration and Deployment server.

This plugin will allow you to send notifications using [Cisco Spark](http://ciscospark.com).

# Usage Examples

## Python

```
python send_message.py <<EOF
{
    "system": {
        "link": "http://drone.mycompany.com"
    },
    "repo": {
        "owner": "octocat",
        "name": "hello-world",
        "full_name": "octocat/hello-world",
        "link_url": "https://github.com/octocat/hello-world",
        "clone_url": "https://github.com/octocat/hello-world.git"
    },
    "build": {
        "number": 1,
        "event": "push",
        "branch": "master",
        "commit": "436b7a6e2abaddfd35740527353e78a227ddcb2c",
        "ref": "refs/heads/master",
        "author": "octocat",
        "author_email": "octocat@github.com"
    },
    "workspace": {
        "root": "/drone/src",
        "path": "/drone/src/github.com/octocat/hello-world",
        "keys": {
            "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC..."
        }
    },
    "vargs": {
        "auth_token": "ZmRmY2..",
        "roomId": "Y2lzY...",
        "message": "# Sending Spark Message \n Using Markdown!!!"
    }
}
EOF
```

## Docker

```
docker run -i hpreston/drone-spark <<EOF
{
    "system": {
        "link": "http://drone.mycompany.com"
    },
    "repo": {
        "owner": "octocat",
        "name": "hello-world",
        "full_name": "octocat/hello-world",
        "link_url": "https://github.com/octocat/hello-world",
        "clone_url": "https://github.com/octocat/hello-world.git"
    },
    "build": {
        "number": 1,
        "event": "push",
        "branch": "master",
        "commit": "436b7a6e2abaddfd35740527353e78a227ddcb2c",
        "ref": "refs/heads/master",
        "author": "octocat",
        "author_email": "octocat@github.com"
    },
    "workspace": {
        "root": "/drone/src",
        "path": "/drone/src/github.com/octocat/hello-world",
        "keys": {
            "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC..."
        }
    },
    "vargs": {
        "auth_token": "ZmRmY2..",
        "roomId": "Y2lzY...",
        "message": "# Sending Spark Message \n Using Markdown!!!"
    }
}
EOF
```

## .drone.yml

```
# Basic Option
notify:
  spark:
    image: hpreston/drone-spark
    auth_token: XXXXXXXXX
    roomId: XXXXXXXXX
    message: "Sample message"

# Room Name Option
notify:
  spark:
    image: hpreston/drone-spark
    auth_token: XXXXXXXXX
    roomName: XXXXXXXXX
    message: "Sample message"

# Send to Email Option
# Basic Option
notify:
  spark:
    image: hpreston/drone-spark
    auth_token: XXXXXXXXX
    personEmail: XXXXXXXXX
    message: "Sample message"


```