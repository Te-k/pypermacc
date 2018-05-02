# pypermacc

Python3 wrapper for the perma.cc API (partial implementation, pull requests welcome)

## Installation

```
git clone https://github.com/Te-k/pypermacc.git
cd pypermaa
pip install .
```

## Usage

**Without private key:**
```py
from pypermacc import Permacc
perm = Permacc()

# Download public archives
archives = p.public_archives()

# Get detail on the first one
details = p.archive_detail(archives['objects'][0]['guid'])

# Download warc file
warc = p.archive_download(archives['object'][0]['guid'])
```

**With a private key**
```py
from pypermacc import Permacc
perm = Permacc(KEY)

# Save a webpage
saved = pp.archive_create('https://perma.cc/') # Inception
```

## License

This code is publised under the MIT license
