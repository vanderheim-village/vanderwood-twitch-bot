The dependency graph of the requirements is as follows:

```
dev +-> prod +-> common
+
|
v
mypy
```

Steps to update a lock file, e.g. to update ipython from 5.3.0 to latest version:

0. Remove entry for `ipython==5.3.0` in dev.txt.
1. Run `./tools/update-locked-requirements`, which will generate new entries, pinned to the latest version.
2. Commit your changes.
