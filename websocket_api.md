# Set-Up
Create a server object in de admin. IP and Daemon port are mandatory. Auth_token gets auto-generated.

Once this is done, you can test the created server on `/serverdebug/1/`

# Connecting

Endpoints are at `hostname/ws_v1/server/<SERVER_ID>`.

After you connect, you need to send an auth packet before you can do anything else. This looks like:

```
{
    "namespace": "auth",
    "data": {
        "token": "107b93521e9989840f43cc721edc946a17cc0541"
    }
}
```

Now you can send data.
