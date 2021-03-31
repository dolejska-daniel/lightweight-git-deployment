# Lightweight Git Repository Deployment
> v0.1

## Introduction
Welcome to this mini-project repository!
The aim of this project is to provide **extensible**, **lightweight** and **easy to configure** webhook processor.
This implementation allows extremely simple webhook event binding and their processing.
Automate anything you want with a _single configuration file_.

The implementation is highly modular and also allows straightforward implementation of custom Python handler scripts.

## Downloading
The easiest way to start is to clone the repository locally and then run it using `pipenv`. 
```shell
# clone the repository
git clone https://github.com/dolejska-daniel/lightweight-git-deployment.git
cd lightweight-git-deployment

# create local configuration
cp config/app.dist.yaml config/app.yaml
cp config/logging.dist.yaml config/logging.yaml

# install dependencies
pipenv install
```

After you have configured all the bindings in the `config/app.yaml` configuration file, start the application by:
```shell
./scripts/start.sh
```

### Requirements
This project requires [`Python >= 3.9`](https://www.python.org/downloads/).
With [`pipenv`](https://pypi.org/project/pipenv/), the project should be working out-of-the-box.

## Usage
The `bindings` key in `config/app.yaml` is of `list[Binding]` type.

**`Binding`**<br>
The `Binding`s are configured by providing corresponding **conditions** and **actions**.
The structure is as follows:

| Key          | Type              | Description                                                              |
|--------------|-------------------|--------------------------------------------------------------------------|
| `conditions` | `list[Condition]` | Binding conditions determining whether the actions should be run or not. |
| `actions`    | `list[Action]`    | Binding actions to be run if conditions are met.                         |

**`Condition`**<br>
The `Condition` definition is of `dict[str, Any]` type.
Its keys refer to fields of the received webhook event.
Its values refer to the required values of the corresponding event field.

```yaml
- created: false
  ref: refs/heads/master
  repository.full_name: dolejska-daniel/lightweight-git-deployment
- sender.id: 10078080
  repository.full_name: dolejska-daniel/lightweight-git-deployment
```

This example defines two `Condition`s.
If any one of the two is met, the actions are run.
For the `Condition` to be met all its rules must evaluate to `true`.
The example will run the binding's action iff:
  - the event is a commit push to repository `dolejska-daniel/lightweight-git-deployment`
  - the event is sent by user with id `10078080` to repository `dolejska-daniel/lightweight-git-deployment`

**`Action`**<br>
The `Action` object defines which actions are to be run iff the conditions were a match.
The structure is as follows:

| Key      | Typ              | Description                                                       |
|----------|------------------|-------------------------------------------------------------------|
| `call`   | `str`            | Defines which method from which module should be called.          |
| `args`   | `list[Any]`      | Defines positional arguments to be supplied to the called method. |
| `kwargs` | `dict[str, Any]` | Defines keyword arguments to be supplied to the called method.    |

```yaml
- call: plugin.git.pull
  args:
    - /opt/torscraper
    - origin
- call: plugin.shell.command
  args:
    - make image
```

This example defines two `Action`s.
First action will run method `pull` in the `plugin.git` module.
This method will perform a `git pull` from provided origin in the given repository.
Then, the second action is run the same way.
The method `plugin.shell.command` simply runs the provided command in a shell. 

### Supported Events

#### GitHub Webhooks
| Name      | Description |
|-----------|-------------|
| `create`  | [API Docs](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#create)
| `delete`  | [API Docs](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#delete)
| `ping`    | [API Docs](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#ping)
| `push`    | [API Docs](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#push)
| `release` | [API Docs](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#release)

