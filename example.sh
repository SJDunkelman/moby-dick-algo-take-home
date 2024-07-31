#!/bin/bash
cat $1 | tr " .,();{}[]" "\n" | sort | grep -v "^$" | uniq -c | sort -nr | head -20