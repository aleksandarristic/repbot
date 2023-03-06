# repbot

A dead-simple slack bot to query SURBL for domain reputation.

### Config

Create your .env file (take a look at .env.sample) and enter your own Slack APP and Slack BOT tokens. Run your bot with ``` python bot.py```.

### Usage

Send a slack dm to your bot with the following contents:

```text
!rep domain.tld
```

or

```text
!rep email@domain.tld
```

Example response:

```text
Domain "test" is on the following blacklists:
 * Phishing
 * Malware
 * Spam and abuse
 * Cracking
```

