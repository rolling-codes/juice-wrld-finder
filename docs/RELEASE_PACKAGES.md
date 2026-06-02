# GitHub Release Packages

GitHub Releases publish three installable ZIP packages. Each package is source-based and includes the files needed for its deployment mode; generated caches, local databases, virtual environments, node modules, coverage output, and private `.env` files are intentionally excluded.

## Packages

- `juice-wrld-finder-desktop-app-view.zip`
  - FastAPI backend, React web app source, built web assets, docs, and shared metadata/import code.
  - Use this for a local desktop browser or packaged desktop-shell deployment of the web experience.

- `juice-wrld-finder-discord-bot.zip`
  - FastAPI backend, Discord bot code, docs, and import/config files.
  - Use this when deploying the bot and backend without the React frontend.

- `juice-wrld-finder-discord-bot-plus-web.zip`
  - Complete backend, Discord bot, React web app source, built web assets, Docker files, docs, and tests.
  - Use this for the full web plus Discord deployment.

## Included Configuration

Release packages include `.env.example` only. Real credentials, local databases, local downloads, and direct private folder links should stay outside release assets. Optional external link integrations remain configurable through environment variables.
