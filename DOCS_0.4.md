Use the Spark plugin to send a notification to a Spark Room when a build completes.  The plugin will send a standard notification to the room including the following details:

---

##Build for {{ repo.full_name }} is Successful

Build author: {{ build.author }}

###Build Details

* Build Log
* Commit Log
* **Branch:** {{ build.branch }}
* **Commit Message:** {{ bulid.message }}

---

You can also specify a **message** in the plugin configuraiton to send an additional custom notification.

You will need to provide the following details to the plug-in

* **auth_token** - A Spark Token for API access
* One of the following to identify the destination room
  * **roomId** - The Spark Room Id for a room
  * **roomName** - The Room Name or Title
  * **personEmail** - An email address for a Spark User

The following is a sample Spark configuration in your .drone.yml file:

```yaml
notify:
  spark:
    image: hpreston/drone-spark
    auth_token: XXXXXXX
    roomName: "Drone Build Notifications"
    message: "Great job on your new build!!"
```
