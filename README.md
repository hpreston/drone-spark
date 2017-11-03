# drone-spark

This is a plugin for [drone.io](http://drone.io), a Continuous Integration and Deployment server.

This plugin will allow you to send notifications using [Cisco Spark](http://ciscospark.com).

***This plugin currently only supports Drone 0.4***

## Drone Version Support

This plugin supports multiple version of Drone within branches and Docker Tags.  

* Drone 0.7
  * Available on GitHub at branch [0.7](https://github.com/hpreston/drone-spark/tree/0.7) and [master](https://github.com/hpreston/drone-spark)
  * Available on Docker Hub as [hpreston/drone-spark:0.7](https://hub.docker.com/r/hpreston/drone-spark/tags/) and [hpreston/drone-spark:latest](https://hub.docker.com/r/hpreston/drone-spark/tags/)
  * May also work with Drone 0.5 and 0.6 but primary testing completed with 0.7
* Drone 0.4
  * Available on GitHub at branch [0.4](https://github.com/hpreston/drone-spark/tree/0.4)
  * Available on Docker Hub as [hpreston/drone-spark:0.4](https://hub.docker.com/r/hpreston/drone-spark/tags/)
  * See [README_0.4.md](README_0.4.md) for details on 0.4
  * See [DOCS_0.4.md](DOCS_0.4.md) for details on 0.4

# Usage Examples

## .drone.yml

See [DOCS.md](DOCS.md) for how to configure and use the plugin.


## Docker

Build the docker image with the following commands.

```bash
docker build -t hpreston/drone-spark .
```

Test the plug-in locally with.

```bash
docker run --rm \
  -e SPARK_TOKEN=ZmRmY... \
  -e PLUGIN_PERSONEMAIL=developer@email.local \
  -e DRONE_REPO_OWNER=octocat \
  -e DRONE_REPO_NAME=hello-world \
  -e DRONE_COMMIT_SHA=7fd1a60b01f91b314f59955a4e4d4e80d8edf11d \
  -e DRONE_COMMIT_BRANCH=master \
  -e DRONE_COMMIT_AUTHOR=octocat \
  -e DRONE_COMMIT_AUTHOR_EMAIL=octocat@email.local \
  -e DRONE_BUILD_NUMBER=1 \
  -e DRONE_BUILD_STATUS=success \
  -e DRONE_BUILD_LINK=http://github.com/octocat/hello-world \
  -e DRONE_TAG=1.0.0 \
  -e CI_COMMIT_MESSAGE="Great Commit" \
  -e CI_BUILD_LINK=http://github.com/octocat/hello-world/compare/775...5562 \
  -e DEBUG=true \
  hpreston/drone-spark
```

# Roadmap and Plans

This plugin is in active development and has the following features planned

* Support for handlebar templating like other notification templates
* Support for referencing the environment variables used by Drone
