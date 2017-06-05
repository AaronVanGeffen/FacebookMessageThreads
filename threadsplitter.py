#!/usr/bin/env python3
import argparse
import os
import sys
import xml.etree.ElementTree as etree


def writeThreadToFile(participants, messages):
    if len(participants) == 0:
        print("    WARNING: no participants in thread -- skipping " + str(len(messages)) + " message(s)")

    # What file are we writing to?
    outputFile = os.path.join(args.outdir, ', '.join(participants) + ".html")

    # New file? Start with basic HTML pleasantries.
    if not os.path.exists(outputFile):
        print("Appending to", outputFile)
        handle = open(outputFile, 'w+')
        handle.write('<!DOCTYPE html><meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        handle.write('<style type="text/css">body { font-family: sans-serif; } .user { font-weight: bold; } .meta { margin-left: 1em; color: #999 } </style>')
        handle.write('<p>Participants: ' + (', '.join(participants)) + '</p>')

    # Otherwise, append to the existing file.
    elif os.path.isfile(outputFile):
        print("  Writing to", outputFile)
        handle = open(outputFile, 'a+')

    # Append each of the messages in order.
    for (header, body) in messages:
        handle.write(header)
        handle.write(body)

    # End with a horizontal rule.
    handle.write('<hr>')
    handle.close()


def processFile(action=writeThreadToFile):
    file = open(args.messages)
    for event, elem in etree.iterparse(file, events=('end', 'start')):
        # Infer our own name if not provided.
        if elem.tag == 'h1' and args.myname == None:
            args.myname = elem.text

        # Process each of the threads individually.
        if 'class' in elem.attrib and elem.attrib['class'] == 'thread':
            participants, messages = processThread(elem)
            action(participants, messages)

        # Free element after use.
        elem.clear()


def processThread(thread):
    messages = []
    participants = []
    savedHead = savedBody = None

    # First, get all messages in this thread.
    for elem in thread.getchildren():
        # Message headers
        if elem.tag == 'div':
            # Keep track of all participants.
            participant = elem.find("./div/span")
            if participant != None and participant.text != None:
                if not participant.text in participants and not participant.text == args.myname:
                    participants.append(participant.text)

            savedHead = etree.tostring(elem, encoding="unicode")

        # Message bodies
        elif elem.tag == 'p':
            savedBody = etree.tostring(elem, encoding="unicode")

        # Store message header and body.
        if savedHead and savedBody:
            messages.append([savedHead, savedBody])
            savedHead = savedBody = None

    # Reverse thread order.
    messages.reverse()

    return (participants, messages)


# Run on command line if not used as a package.
if __name__ == '__main__':
    # Parse arguments from command line.
    parser = argparse.ArgumentParser(description='Split message threads into their own files')
    parser.add_argument('--messages', dest='messages', required=True,
                        help='HTML file from which to read messages')
    parser.add_argument('--outdir', dest='outdir', required=True,
                        help='Folder to write message threads to')
    parser.add_argument('--myname', dest='myname', required=False, default=None,
                        help='Name to ignore when naming conversations')

    args = parser.parse_args()

    # Create output directory if needed.
    if not os.path.isdir(args.outdir):
        if not os.path.exists(args.outdir):
            print("Output dir " + args.outdir + " does not exist yet, creating...")
            os.makedirs(args.outdir)
        else:
            print("Specified output dir " + args.outdir + " is not a directory...")
            sys.exit(1)

    # Sanity check: does our input file exist?
    if not os.path.isfile(args.messages):
        print("Input file dir " + args.messages + " does not exist yet, creating...")
        sys.exit(2)

    # Process the file.
    processFile()
