# Captain Webhook

Captain Webhook is a very simple Python script that will run an HTTP server and trigger commands whenever a secret URL
is requested. It is mainly used for deployments, for example triggering ansible-pull whenever a commit is pushed to
GitHub.

## Installing

You can install Captain Webhook using `pip`:

```
pip install captainwebhook
```

You can also get the latest source at the canonical location of Captain Webhook, its GitHub repository:

[https://github.com/skorokithakis/captainwebhook](https://github.com/skorokithakis/captainwebhook)


## How to use

Using Captain Webhook is very simple. Just launch it with the command you want to run:

```
cptwebhook "echo hello!"
```

And visit the URL in your browser:

[http://localhost:48743/webhook/changeme/](http://localhost:48743/webhook/changeme/)

The command you specified will be run.


## "Advanced" options

Captain Webhook supports some super-advanced functionality that is detailed
below.

### Password protection

Obviously, the URL above isn't very secure, since anyone could trigger the command then. To make things a bit more
obscure, and thus secure, Captain Webhook allows you to specify a key:

```
cptwebhook -k ichoKie5IeGhiexa "echo hello!"
```

The URL now becomes:

[http://localhost:48743/webhook/ichoKie5IeGhiexa/](http://localhost:48743/webhook/ichoKie5IeGhiexa/)

### Command templates

Your command doesn't have to be static! Captain Webhook can accept template
variables in the command string and populate them with whatever comes in the
query string of the request by passing the `--template` flag. For example:

```
cptwebhook -t "echo Hello, {name}!"
```

Try the URL:

[http://localhost:48743/webhook/changeme/?name=world](http://localhost:48743/webhook/changeme/?name=world)

will execute "echo Hello, world!". Isn't that the best thing ever?

### Miscellanea

Other options include the interface and port the server will listen on. You can see more details with:

```
cptwebhook -h
```


## Miscellaneous

Captain Webhook will always return a 200 (some services don't like other return codes), and will always return JSON.
A command will never be triggered again while the first one is running, Captain Webhook will just ignore any subsequent
invocations until the first one is finished.
