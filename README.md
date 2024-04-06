# sliver

This is a set of Mythic agents for interacting with [Sliver](https://sliver.sh/) C2 framework.

- `sliverapi`: for interacting with the sliver server (ie: start listeners, list sessions...etc)
- `sliverimplant`: for interacting with a sliver implant (ie: ps, netstat...etc)

The SliverAPI payload doesn't build anything, but instead generates a "callback" within Mythic that allows you to interact with Sliver's API. This requires you to generate an [operator configuration file](https://sliver.sh/docs?name=Multi-player+Mode). This config file is the only build parameter, and once built, a callback will immediately appear.

A SliverImplant callback is instantiated when tasking a `use -id <sliver_implant_id>` from within the SliverApi callback. 

## Future Plans / Ideas

- Better integration with all Mythic features
  - especially UI improvements with results / data
  - interactive commands
  - documentation-payload
- Build sliver implant payloads through Mythic
- sliver 3rd party integrations?
- Sync to just create all callbacks / auto create+track them
  - since sliver can still be used normally without mythic
- Ability to run the sliver server within mythic?

### Fixes / TODOs

- make Dockerfile build faster / fix grpc error
- parity with all commands in sliver
- write a blog post about experience / video demo?

## How to install an agent in this format within Mythic

When it's time for you to test out your install or for another user to install your agent, it's pretty simple. Within Mythic is a `mythic-cli` binary you can use to install agents:

- `sudo ./mythic-cli install github https://github.com/user/repo` to install the main branch
- `sudo ./mythic-cli install github https://github.com/user/repo branchname` to install a specific branch of that repo

Now, you might be wondering _when_ should you or a user do this to properly add your agent to their Mythic instance. There's no wrong answer here, just depends on your preference. The three options are:

- Mythic is already up and going, then you can run the install script and just direct that agent's containers to start (i.e. `sudo ./mythic-cli payload start agentName` and if that agent has its own special C2 containers, you'll need to start them too via `sudo ./mythic-cli c2 start c2profileName`).
- Mythic is already up and going, but you want to minimize your steps, you can just install the agent and run `sudo ./mythic-cli mythic start`. That script will first _stop_ all of your containers, then start everything back up again. This will also bring in the new agent you just installed.
- Mythic isn't running, you can install the script and just run `sudo ./mythic-cli mythic start`.

## Local Development Notes

<!-- TODO: clean this up with better notes, starting with requirements and 'git clone' (all steps) -->

- VSCode devcontainer

  - If using vscode, it will prompt to auto build and attach to the Docker file
    - Warning: building the container takes a few minutes! (TODO: fix this)
  - Auto adds the suggested extensions / settings
  - Use the debugger for breakpoints! (and easy restart of the main.py process)

- Required commands for local development against remote mythic

```bash
# In Mythic
sudo ./mythic-cli config set rabbitmq_bind_localhost_only false
sudo ./mythic-cli config set mythic_server_bind_localhost_only false
sudo ./mythic-cli restart

# get the RABBITMQ_PASSWORD from .env and paste into a rabbitmq_config.json
# In this repo
cd ./Payload_Type/sliverapi
cp rabbitmq_config.json.example rabbitmq_config.json
```

<!-- TODO: describe example setup with ubuntu vm running both mythic and sliver -->

Once inside the container and rabbitmq set

```bash
# or instead of running manually, hit the debug play button in vscode!
cd ./Payload_Type/sliverapi/
python3 main.py
```

### Current Work TODOs

- difference between session and beacon
  - different ways of calling the sliver-py api
- refactor sliver api into 1 place?
- exit command (for the callbacks?)
  - sliver can close the sessions / exit interactive?
