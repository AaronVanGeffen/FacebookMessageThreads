# Facebook Message Thread Splitter

This repository contains a Perl script I used to split Facebook conversations by thread, using the `messages.htm` file found in your Facebook data archive.

As the `messages.htm` file can grow pretty massive, depending on your Facebook activity, it cannot be viewed or searched easily. This script aims to fix that by splitting the file based on what Facebook reports as a message thread.

Furthermore, it outputs the threaded messages chronologically for natural reading, instead of the reverse order provided.

## Usage
```
$ ./threadsplitter.pl path/to/facebook/dump/messages.htm conversations/
```

This will read messages.htm from path/to/facebook/dump and store the threads in separate files by conversation.

## Licence

I am releasing this code under the BSD 2-clause licence as found on http://opensource.org/licenses/BSD-2-Clause
