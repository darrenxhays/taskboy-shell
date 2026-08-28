# skills/

Installed skills live here, one directory per skill: `skills/<name>/SKILL.md`. The `taskboy setup` wizard's skills picker fills this directory from the packaged templates; to install one by hand, run `taskboy assets templates /tmp/seed`, copy a template directory here, and replace every `{{variable}}` placeholder (the variable table is in the extracted `templates/skills/README.md`).

The deploy workflow ships this directory to the host alongside `config/`. Skills are also editable live from the dashboard's Config page.
