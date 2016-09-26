# drone-spark

This is a plugin for [drone.io](http://drone.io), a Continuous Integration and Deployment server.

***This plugin currently only supports Drone 0.4***

This plugin will allow you to send notifications using [Cisco Spark](http://ciscospark.com).

# Usage Examples

## .drone.yml

See [DOCS.md](DOCS.md) for how to configure and use the plugin.

## Python

```
python send_message.py <<EOF
{
    "system": {
        "link_url": "http://drone.mycompany.com"
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
        "author_email": "octocat@github.com", 
        "link_url": "https://github.com/octocat/hello-world",
        "message": "Testing...",
        "status": "success"
    },
    "workspace": {
        "root": "/drone/src",
        "path": "/drone/src/github.com/octocat/hello-world",
        "keys": {
            "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC..."
        }
    },
    "vargs": {
        "message": "# Sending Spark Message \n Using Markdown!!!",
		"auth_token": "ZmRm....",
		"roomName": "ROOM NAME"
    }
}
EOF
```

## Docker

```
docker run -i hpreston/drone-spark <<EOF
{
    "system": {
        "link_url": "http://drone.mycompany.com"
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
        "author_email": "octocat@github.com", 
        "link_url": "https://github.com/octocat/hello-world",
        "message": "Testing...",
        "status": "success"
    },
    "workspace": {
        "root": "/drone/src",
        "path": "/drone/src/github.com/octocat/hello-world",
        "keys": {
            "private": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC..."
        }
    },
    "vargs": {
        "message": "# Sending Spark Message \n Using Markdown!!!",
		"auth_token": "ZmRm....",
		"roomName": "ROOM NAME"
    }
}
EOF
```

# Roadmap and Plans

This plugin is in active development and has the following features planned

* Support for Drone 0.5
* Support for handlebar templating like other notification templates
* Support for referencing the environment variables used by Drone