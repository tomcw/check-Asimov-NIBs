# check-Asimov-NIBs

Pre-requisites:
- python 3.8.5
- pip install requests
- create 2 subfolders: `NIBs` & `NIBZIPs`
- download `site_index.txt` from [here](https://mirrors.apple2.org.za/ftp.apple.asimov.net/)

Limitations:
- zipped .nibs are skipped (but copied to `NIBZIPs`)
- there are a few false-positive matches for .nibs (eg. MoonPatrol.nib.asm, threshold.nib.readme), which are harmless
