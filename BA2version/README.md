# BA2 Archive header changer

Switches Bethesda archive version between versions 1(Fallout 4, 76), 7(Fallout 4 NG), and 8(Fallout 4 NG).

Probably could be turned into a pip module and be invoked without the python script name.

### Examples:
View (and save) archives and versions:

```bash
python BA2version.py -d "Fallout 4\Data" --view
```

Set version of archives listed in input.csv(version column in input.csv is ignored) to version 1

```bash
python BA2version.py -d "Fallout 4\Data" --change 1
```
Restore only Fallout 4 ba2 archive headers to original NG versions

```bash
python BA2version.py -d "Fallout 4\Data" --restore
```

Specify which backup to restore

```bash
python BA2version.py -d "Fallout 4\Data" --restore fallout
```

Dry run (Don't modify any files, just show changes) for any of the above commands: Add -t or --test

```bash
python BA2version.py -d "Fallout 4\Data" --restore fallout --test
```

```bash
python BA2version.py -d "Fallout 4\Data" --restore full --test
```

```bash
python BA2version.py -d "Fallout 4\Data" --change 7 --test
```