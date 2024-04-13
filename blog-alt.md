# Alternative Blog

- blog in the style of 'lets do this together' (and don't mention mistakes / struggles)

- here's an idea, lets see if its possible

## Step 1 - Defining our goals

- "In Mythic, I want the ability to control the Sliver server, start listeners, build implants, etc..."
- "In Mythic, I want a sliver implant callback, I want to issue an 'ls' task, see the results, and show them in the file browser"

## Step 2 - Research and Planning

### Read the Docs

- Lets readup on Sliver's documentation & Mythic's documentation
    - how do they work, how does information flow, how to make a custom agent?
    - similar agents (bloodhound, nemesis, ghost)✅

- Lets join a forum to ask questions and see what others are doing
    - reaching out to the devs
    - "is my idea feasbile?" (yes!) ✅

### System Design

- now that we sorta know how things work, where will our solution fit?
    - assumption == external sliver server with implants already calling back to it
        - avoid "before using this agent, do these weird things with sliver to make it compatible"

- Which flow to use? (information flow / networking)
    - Sliver C2 handled by Mythic (avoid needing sliver server, but too hard to re-implement for me)
    - Mythic using the Sliver cli tool (full functionality, but sounds gross and full of string parsing results)
    - Mythic connecting to Sliver's gRPC✅

- ok, but how to connect? (gRPC is supported by multiple languages)
    - sliver-script (I'm most familiar with TS, but it seems outdated, Mythic doesn't support it)
    - make our own go client (I don't know go, but sliver's cli client is written in go, and Mythic supports go)
    - sliver-py (I know python, its updated, and Mythic supports it!)✅

## Step 3 - Initial Testing

- lets play around with sliver-py, don't worry about Mythic right now
    - ubuntu 22 VM with sliver installed
    - generate config and start by following the readme example
    - running locally (in container), fixing the grpc bug
        - read the github issues, ask some questions, got it!
    - try a custom command not in the readme example (generate implant)
        - learning gRPC as we play around
        - got it! (can write the response to a file) ✅

- lets play around with Mythic
    - add Mythic to the same ubuntu 22 VM, login
    - jupyter notebooks might be the answer
        - can connect to sliver
        - run generate implant
        - learning how to talk to mythic, save implant file to Mythic DB ✅

## Step 4 - Implementing

- what is a good developer setup for Mythic?
    - devcontainer + rabbitmq

### sliverapi agent Payload_Type

- Follow the example agent walkthrough + copying what bloodhound did
    - stick to bare minimums
- able to build, give config file, create api callback
- add a simple command 'sessions'
- add more commands, learning mythic arguments ('beacons', 'profiles') (sticking with sliver things I know)
- add 'use' which will create an implant callback

### sliverimplant agent Payload_Type

- ensure beacons vs sessions are good
- simple commands - 'ifconfig', 'netstat', 'pwd'
- commands that integrate with Mythic - 'upload', 'download'
- supported_ui features
    - process_browser - 'ps'
    - file_browser - 'ls'
- interactive tasking - 'shell'
    - not supported by sliver-py!
    - ask more questions, reference sliver-script and go client
    - learn more about gRPC, async python
    - request more features from Mythic

## Step 5 - Profit

- we've reached our end goal! (and even added bonus features)
- clear path for adding more functionality
    - full parity with sliver client
        - can improve output formatting
        - can better match command arguments (TODOs)
- lots of ideas on how to improve
    - switch to 'go' to more easily copy from Sliver cli
    - portfwd, proxy, 3rd party commands
    - auto sync callbacks (if it pops up in sliver, it will popup in mythic)
    - run sliver server within Mythic?

