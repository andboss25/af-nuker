# AF NUKER

Af nuker or Antifurry nuker is a template based proxyless easy to use nuke bot based on the discord api wrapper that i made: [Anticord](https://github.com/andboss25/anticordpy).
Af nuker might be slow scince it dosent use proxy : it is proxyless , anticord is based onto the use of templates that makes it special , that might change soon because im planning to add proxies to Af nuker.

# HOW TO USE

(This is in the AFNuker folder)
Once you have downloaded all files:
1. Run this command in cmd: `Pip install -r requirements.txt`
2. Put your token in token.txt (Bot might need privileged gateway intents)
3. Run main.py with python
4. Type help for a list of commands

# TEMPLATES

Templates allow you to change the nuke content easaly without needing to modify the code:
A template must have the .afnk file extension

Example afnuker template:
`# Antifurry template
[ guild-rename -> name : Raped by antifurry ]
[ channel-nuke -> name : fucked-by-antifurry ]
[ channel-rename -> name : fucked-by-antifurry ]
// This is cool
[ message-nuke -> message : Get fucked by antifurry @everyone https://tenor.com/view/anti-furry-afa-animated-antifur-gif-25154410 ]`

`# = Title`
`// = Comment`
`[] = Ruleset`

Rulesets will define a value of the nuke , like the message spammed in the nuke
They can have 2 operators:

`: - Define a rule`
`-> - Specify what propiety you define the rule in`

Values can be booleans or strings:

`Boolean - |&True`
`String - Furries fucking suck`

You can see a list of values and what can you modify inside a template in main.py

Rulesets must not be:
`[guild-rename -> enabled : |&True]`
They need to be:
`[ guild-rename -> enabled : |&True ]`
