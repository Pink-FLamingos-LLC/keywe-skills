# Skills Repo

AI agent skills for property management and smart lock automation.

## Skills

- **keywe** — Set up and automate vacation rental properties, Schlage smart locks, guest messaging, reservations, and access codes. Guides users through creating an API key, configuring a `.env` file with credentials, authenticating Schlage, provisioning properties/locks, and integrating lock control into applications.

## Usage

Skills are loaded by an AI agent (e.g., opencode, Claude) to provide domain expertise and workflows. Each skill is in `skills/<name>/` with a `SKILL.md` entry point and supporting references/scripts.

When an agent loads the **keywe** skill, it will walk the user through:

1. Creating a KeyWe account and generating an API key
2. Creating a `.env` file with `KEYWE_API_KEY`, `SCHLAGE_EMAIL`, and `SCHLAGE_PASSWORD`
3. Running the client script to authenticate with Schlage
4. Provisioning properties, access points, and locks
5. Making API calls to lock/unlock doors

## Adding a Skill

Create a new directory under `skills/<name>/` with at minimum a `SKILL.md` file.
