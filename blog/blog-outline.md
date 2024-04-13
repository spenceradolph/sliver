# Blog (Outline)

- blog in the style of 'this is the story from my perspective'

- summary sentence / announce release of agents?
- What will this post be about
    - experience in research and development
    - problem solving

## Intro

### Background

- talk about using Sliver (some team members wanted Mythic instead)
- What is Sliver
- what is Mythic

### Idea + End Goal

- why not get the best of both worlds?
- end state == task a sliver implant 'ls' and see the results in mythic's process browser

## Research

- Don't know what to do until research is done, is it feasible?
    - feasible also means I can do it, I'm ok with python
- How does Sliver work? (documentation) (rpc?)
- How does Mythic work? (documentation / youtube)
- Reaching out to Mythic's creator on twitter -> finding the slack
    - now I can ask more detailed questions!
    - first Q: https://bloodhoundhq.slack.com/archives/CHG769BL2/p1710799610153789

- should sliver agents traffic reach into a mythic listener and be tasked from that instead of sliver server?
    - probably not
- should I at worst case just use the sliver-client cli through some sort of terrible python subprocess?
    - that sounds nasty

- show chart of options to work with?
    - sliver can have any gRPC supported language, but offers a python and typescript pre-built client
    - mythic can be written in go or python

Sliver at one point appears to have started a [gui](https://github.com/BishopFox/sliver-gui), but it appears to have been discontinued. 

### Initial Testing

- Kali Setup (but then Ubuntu) (confusion with Dockerfile)
    - install Sliver, install Mythic, snapshot
- struggles with sliver-py, but eventual success
    - read github issues and try everything!
    - ask questions
- Working with Jupyter
    - able to interact, able to build implants

## First Implementations

### sliverapi

- Following the example agent walkthrough + research into 3rd party agents (bloodhound, etc...)
- able to build, give config file (text vs file)
- 'get_sessions' working!
- moving from the VM to a devcontainer (rabbitmq)
    - good thing I asked about it!
    - debugging setups
- adding more commands, learning mythic arguments ('beacons', 'profiles') (sticking with sliver things I know)

### sliverimplant

- implant type finally added, can task 'ifconfig', 'ls', 'ps'
- more complex things 'upload', 'download'
- beacons vs sessions

## Problem Solving

- shell isn't in sliver-py, but I wanted it cause cool-factor + mythic ui support
    - trying to figure it out through the debugger and guessing with intellisense
    - trying to figure it out by looking at the go client
    - asking sliver devs! (slightly helpful) (see their profile pics match)
    - almost switching project entirely to go
    - wow, sliver-script implements it! (why didn't I check there earlier)
    - learning about gRPC and async python
    - manually spawning shell and sending commands
    - manually reading results
        - had to restart everything (bugs?)
    - simple loop to read and write
    - finally an async loop for stdin
    - how to get things from mythic?
        - talked with mythic dev
        - logger!
    - working implementation!

### When is it me and when is it the tools?

- talk about continued integrations with supported_ui
    - actually found some bugs within Mythic
        - awesome support from its_a_feature_ <3
    - can still help as a non-go dev, reading code is a skill for any language
- vigilant watching of logs (mythic has nice logging)
- follow debug code as far as you can
- always restart everything if you can (things can linger)

## Conclusion

- I met my end-goal that I began with
    - learned a lot about how both Sliver and Mythic work
- Clear path for continuing to add functionality
    - get closer to matching sliver's cli (command parameters)
    - adding commands is easy
- Lots of fun ideas for the future
    - re-implement in go
    - run sliver within mythic
    - harder problems like portfwd / proxy / sliver 3rd party things

- what skills did I use?
    - experience as a developer (mostly web)
        - docker, linux, networking, VM's, python
    - experience with good development workflows (if its clunky, improve it)
        - debugging + vscode devcontainers > print statements within InstalledServices
    - 
