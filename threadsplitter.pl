#!/usr/bin/perl
use strict;
use warnings;
use v5.10;

use Data::Dumper;
use File::Slurp;
use Mojo::DOM;

use constant MY_NAME => "Aaron van Geffen";

my ($filename) = shift;
my ($export_dir) = shift;
if (!$filename or !(-f $filename) or !$export_dir) {
	warn "Usage: $0 <path to messages.htm> <directory to export to> \n";
	exit 1;
}

if (!(-d $export_dir)) {
	warn $export_dir, " does not exist -- will now be created.\n";
	mkdir $export_dir;
}

say "Reading file " . $filename . "...";
my $messages = read_file($filename);

say "Parsing DOM structure...";
my $dom = Mojo::DOM->new($messages);

say "Finding threads...";
my $collection = $dom->find('div.thread');

say "Found " . $collection->size . " threads...";
if ($collection->size == 0) {
	say "Nothing to do -- stopping.";
	exit;
}

say "Exporting conversation threads to " . $export_dir . "...";
my %conversations;
for my $conversation ($collection->each) {
	my @conversation_partners = grep(!/@{[MY_NAME]}/, split(', ', $conversation->text));
	my $conversation_name = join(', ', @conversation_partners);

	if (defined($conversations{$conversation_name})) {
		$conversations{$conversation_name}++;
		$conversation_name .= ' - ' . $conversations{$conversation_name};
	} else {
		$conversations{$conversation_name} = 1;
	}

	open SPLITMSG, ">", $export_dir . "/" . $conversation_name . ".htm";
	print SPLITMSG '<!DOCTYPE html><meta http-equiv="Content-Type" content="text/html; charset=utf-8">';
	print SPLITMSG '<style type="text/css">body { font-family: sans-serif; } .user { font-weight: bold; } .meta { margin-left: 1em; color: #999 } </style>';

	my $messages = $conversation->children->reverse;
	my $next_is_header = 0;
	my $previous;

	for my $message ($messages->each) {
		if ($next_is_header) {
			print SPLITMSG $message->to_string;
			print SPLITMSG $previous->to_string;
			$next_is_header = 0;
		} else {
			$previous = $message;
			$next_is_header = 1;
		}
	}

	close SPLITMSG;
}
