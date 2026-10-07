# Possible memory and fd leak in BUpdaterSlurm

- URL: https://github.com/prelz/BLAH/issues/16
- Repo: prelz/BLAH (language: C)
- State: open; created 2017-06-15T09:24:06Z; status ok; passes offcwe

## Issue body

reporter (COLLABORATOR) · drebatto · 2017-06-15T09:24:06Z · https://github.com/prelz/BLAH/issues/16

When the BNotifierSlurm cannot access the registry (e.g. because of wrong ownership, see [GGUST Ticket #128229](https://ggus.eu/index.php?mode=ticket_info&ticket_id=128229)), it leaks memory and keeps a huge number of open files.
