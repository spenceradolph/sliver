# sliver

This is a Mythic agent for interacting with [Sliver](https://sliver.sh/) C2 framework.

This doesn't build a payload, but instead generates a "callback" within Mythic that allows you to interact with Sliver's API. This requires you to generate an [operator configuration file](https://sliver.sh/docs?name=Multi-player+Mode).

This config file is the only build parameter. Once built, a callback will appear that can be tasked to interact with Sliver.

## How to install an agent in this format within Mythic

When it's time for you to test out your install or for another user to install your agent, it's pretty simple. Within Mythic is a `mythic-cli` binary you can use to install agents:

- `sudo ./mythic-cli install github https://github.com/user/repo` to install the main branch
- `sudo ./mythic-cli install github https://github.com/user/repo branchname` to install a specific branch of that repo

Now, you might be wondering _when_ should you or a user do this to properly add your agent to their Mythic instance. There's no wrong answer here, just depends on your preference. The three options are:

- Mythic is already up and going, then you can run the install script and just direct that agent's containers to start (i.e. `sudo ./mythic-cli payload start agentName` and if that agent has its own special C2 containers, you'll need to start them too via `sudo ./mythic-cli c2 start c2profileName`).
- Mythic is already up and going, but you want to minimize your steps, you can just install the agent and run `sudo ./mythic-cli mythic start`. That script will first _stop_ all of your containers, then start everything back up again. This will also bring in the new agent you just installed.
- Mythic isn't running, you can install the script and just run `sudo ./mythic-cli mythic start`.
