# MelonWiki

The MelonLoader Wiki source code

## Contributing

*Most* of the docs are just straight md files and it's as easy as editing the md file and making a pull request to contribute.
Do note that if you want to add a new page, make sure to add an entry to `docs/_sidebar.md`.

If you would like to locally host the docs on your own machine, simply download [docsify](https://docsify.js.org/#/) and call `docsify serve` in the docs folder, and docsify will do the rest for you.

Eventually, an API reference will be made for the wiki. Once that happens, if there are any issues with it, it would be easier for you to create an issue on this repo, rather than opening a pull request, because many docs files are generated using Python scripts (if you figure out how to use them feel free to open a pull request). Meaning it would likely be easier to regenerate the file using the script than manually changing it.
