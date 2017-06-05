# Facebook Message Thread Splitter

This repository contains a Python script that can be used to split Facebook conversations by thread, using the `messages.htm` file found in your Facebook data archive. Over time, this file can grow pretty massive, meaning it cannot be easily viewed or searched.

The script aims to improve the situation by splitting the file based on threads, as reported by Facebook, and their participants. Furthermore, it outputs the threaded messages chronologically for natural reading, instead of the reverse order provided.

## Requirements

A reasonably recent version of a Python 3 interpreter. Python 2 is untested. The script does not require you to install external dependencies.

## Usage
```
$ ./threadsplitter.py --messages path/to/facebook/dump/messages.htm --outdir conversations/
```

This will read `messages.htm` from `path/to/facebook/dump` and store its threads in separate files into `conversations`.

## Licence

I am releasing this code under the BSD 2-clause licence as found on https://opensource.org/licenses/BSD-2-Clause
