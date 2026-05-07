# FlavorOS Vault Plugins

Obsidian community plugins are installed per vault in this folder:

```text
vault/.obsidian/plugins/<plugin-id>/
```

Each plugin folder should contain at least:

```text
manifest.json
main.js
```

and optionally:

```text
styles.css
```

Run this macOS script from the repo to install/update the plugin folders and open the FlavorOS Canvas:

```bash
scripts/open-flavoros-obsidian.command
```

The plugin registry lives at:

```text
vault/.obsidian/flavoros-plugin-registry.json
```

