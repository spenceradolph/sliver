# My Journey on Integrating Sliver into Mythic

There are certainly a lot of C2 frameworks available to choose as a pentester. You might even consider running a [contest](https://commoninja.site/atomics-on-a-friday) to decide which is best. 

Clearly Mythic and Sliver are top-tier, but which should you use? What if you didn't have to decide? I wanted to find out what it would take to just use Mythic to control Sliver. 

Quick and easy project right?

- rick and morty quick adventure meme here

### Background

What is [Sliver](https://sliver.sh/)? 
```
Sliver is a powerful command and control (C2) framework designed to provide advanced capabilities for covertly managing and controlling remote systems. With Sliver, security professionals, red teams, and penetration testers can easily establish a secure and reliable communication channel over Mutual TLS, HTTP(S), DNS, or Wireguard with target machines.
```

What is [Mythic](https://docs.mythic-c2.net/)?
```
Mythic is a multiplayer, C2 platform for red teaming operations. It is designed to facilitate a plug-n-play architecture where new agents, communication channels, and modifications can happen on the fly. Some of the Mythic project's main goals are to provide quality of life improvements to operators, improve maintainability of agents, enable customizations, and provide more robust data analytic capabilities to operations
```

So while Sliver provides and 'all in one' solution for building and managing implants, Mythic by default only provides an 'agnostic' architecure for controlling any [compatible implant](https://github.com/MythicAgents) over any [compatible communication](https://github.com/MythicC2Profiles). You install which agents and profiles you want to use, and can add your own custom ones as well. 

Not only that, but Mythic provides awesome UI to view data that's pulled back from targets, for example a [file browser](https://docs.mythic-c2.net/operational-pieces/file-browser). I didn't yet know how, but I really wanted to type 'ls' into Mythic instead of the Sliver cli and see that awesomeness.

- image of file browser?

## Step 1 - Research

Ok, I have my end goal in mind, but how do I start? When in doubt, read all the documentation you can! 

I started with learning about [Sliver's Architecture](https://sliver.sh/docs?name=Architecture). Looks like there's a client that connects to a server using gRPC. There's even a page on how to create a [Custom Client](https://sliver.sh/docs?name=Custom+Clients). Sweeeeeet. 

Time to get smart on Mythic. The [documentation](https://docs.mythic-c2.net/) is pretty spectacular, but I learned a lot from [this video](https://www.youtube.com/watch?v=xdmdHMjK1KA) on creating a custom agent, and [this video](https://www.youtube.com/watch?v=eL0y73FNrNI) showing some awesome features. Youtube is basically where I learn everything.

I didn't want to do this alone, so I did what anyone would do and DM'd the creator of Mythic [@its_a_feature_](https://twitter.com/its_a_feature_?lang=en) directly.

- image of twitter dm

Through some further research there, I confirmed my idea was technically feasible, and that I could reference a few similar agents that were designed as 3rd party service integrations ([bloodhound](https://github.com/MythicAgents/bloodhound), [ghostwriter](https://github.com/MythicAgents/ghostwriter), [nemesis](https://github.com/MythicAgents/nemesis)).

## Step 2 - Planning

Now that I sorta know how things work, where exactly would my solution fit? 

One assumption I wanted to make was that the sliver server was already up and running with active implants. I didn't want my solution to require any changes to how sliver was installed, and allow operators to continue using Sliver like normal. This meant I was squarely within the domain of Mythic. 

### What is the flow?

In order to type 'ls' and get results, that task needs to get to the implant and return. After some thought, I came up with 3 possible scenarios.

1) Sliver C2 handled by Mythic
    - pros: Avoids needing the sliver-server
    - cons: Way to hard for me to implement
2) Mythic could use the existing sliver-client
    - pros: Fully functional
    - cons: sounds gross and full of string parsing hell
3) Mythic can connect to the sliver-server using gRPC
    - pros: no functional limitations

### gRPC? The What?

I haven't really used gRPC, though I sorta know why it exists and how its used by teams. But how would I go about using it? Sliver offers a few pre-cooked [choices](https://sliver.sh/docs?name=Custom%20Clients), and even a [discontinued gui controller](https://github.com/BishopFox/sliver-gui).


1) [sliver-script](https://github.com/moloch--/sliver-script) (typescript)
    - pros: I have a lot of experience with TS
    - cons: this repo is very outdated
    - cons: Mythic doesn't support TS
2) I could write a custom client in go
    - pros: Mythic supports go!
    - pros: Would be easy to copy from [sliver-client](https://github.com/BishopFox/sliver/tree/master/client)
    - cons: I don't know go 😢
3) [sliver-py](https://github.com/moloch--/sliver-py)
    - pros: Mythic supports python!
    - pros: It's updated
    - pros: I know python fairly well!

## Step 3 - Initial Testing

Cool cool cool. Time to get my hands dirty with code. I spun up a fresh Ubuntu 22 VM, created some snapshots, and installed Sliver. Then I [generated](https://sliver.sh/docs?name=Multi-player%20Mode) an operator config so that I could connect to it remotely using sliver-py. 

- meme about things going downhill?

Sliver-py was having an extremely difficult time connecting. I found the [known issue](https://github.com/moloch--/sliver-py/issues/28) in the github, but took me probably longer than it should to implement the fix. 

The readme mentioned the error and gave a one line fix that didn't work. Another comment titled "I got a better fix!" didn't work, and I was hesitant to try their earlier fix. Turns out, their [first comment](https://github.com/moloch--/sliver-py/issues/28#issuecomment-1469011869) in the thread was the only one that managed to work for me. Yay.

### Walk before Running

Once I had the readme example usage working, next step was to try something a little more custom. Something like generating an implant. Luckily, this wasn't too difficult using vscode's intellisense and a little trial and error. 

- code sample of generating client

Confident in my abilities, I maneuvered into Mythic. Once it was installed on the same VM, I logged into the Jupyter service to try and get things going manually. There were plenty of example scripts interacting with Mythic's RPC's to inspire me. I pasted my code in and I was quickly able to generate an implant, and then upload that binary into Mythic for tracking and "click to download". 

## Step 4 - Implementing (for realz)

Before starting a more official repo, I reached out again to @its_a_feature_ since I was a little confused on the proper agent development setup. Turns out I could develop and run the code externally, and just connect to Mythic using [rabbitmq](https://docs.mythic-c2.net/customizing/payload-type-development#id-3.2-required-folder-structure). 

Should probably be reading all the words...

Knowing this, I opted to use a [VSCode Devcontainer](https://code.visualstudio.com/docs/devcontainers/containers). I could easily have the base container be the one mythic [provides](https://docs.mythic-c2.net/customizing/payload-type-development#id-3.1-dockerfile) for agent development. With this, anyone could clone the repo, and it would prompt to automatically build and attach to a container with all the required tools.

### sliverapi agent

I closely followed the tutorial for a basic agent, and cross referencing the bloodhound agent for any weirdness in being a 3rd party agent. Wasn't long before I could build my agent, which triggered a callback, which could then be tasked. 



