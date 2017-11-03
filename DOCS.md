Use the Spark plugin to send a notification to a Spark Room as part of your pipeline.  The plugin will send a standard notification to the room including the following details:

---

##Build for {{ repo.full_name }} is Successful

Build author: {{ build.author }}

###Build Details

* Build Log
* Commit Log
* **Branch:** {{ build.branch }}
* **Commit Message:** {{ bulid.message }}

---


The following is a simple Spark configuration in your .drone.yml file:

```yaml
pipeline:
  spark:
    image: hpreston/drone-spark:0.7
    personEmail: developer@email.local
    secrets: [ SPARK_TOKEN ]
```

You can also provide an additional custom message to be sent along with the standard build details.  

```yaml
pipeline:
  spark:
    image: hpreston/drone-spark:0.7
    personEmail: developer@email.local
    message: Great Job on the New Build!
    secrets: [ SPARK_TOKEN ]
```

Instead of providing an individual email to send message to, you can provide a roomName or roomId.

```yaml
pipeline:
  spark:
    image: hpreston/drone-spark:0.7
    roomName: Build Reports
    secrets: [ SPARK_TOKEN ]
```

To send the destination via secrets, use this format.  *Note: Only one of the three destination types is required.*

```yaml
pipeline:
  spark:
    image: hpreston/drone-spark:0.7
    secrets: [ SPARK_TOKEN, ROOMNAME, PERSONEMAIL, ROOMID ]
```

# Secrets

The drone-spark plugin requires reading the Spark token from the secrets store within Drone.  Add your SPARK_TOKEN secret with:

```bash
drone7 secret add --name SPARK_TOKEN --value ZmRmY... --repository myorg/myproject --image hpreston/drone-spark:0.7
```

If you'd prefer to provide the destination (personEmail, roomId, or roomName) as a secret than parameter, add them with:  

```bash
drone7 secret add --name PERSONEMAIL --value developer@email.local --repository myorg/myproject --image hpreston/drone-spark:0.7

drone7 secret add --name ROOMID --value YNDX... --repository myorg/myproject --image hpreston/drone-spark:0.7

drone7 secret add --name ROOMNAME --value "Build Info" --repository myorg/myproject --image hpreston/drone-spark:0.7
```

# Parameter Reference

* One of the following to identify the destination room
  * **roomId** - The Spark Room Id for a room
  * **roomName** - The Room Name or Title
  * **personEmail** - An email address for a Spark User
* **message** - *Optional* Additional custom message
* **SPARK_TOKEN** - Authentication Token for Cisco Spark provided via Drone Secret
* **debug** - Optional plugin parameter.  If set the plugin will print out informational details.  
