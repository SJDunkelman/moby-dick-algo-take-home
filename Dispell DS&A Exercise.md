# Dispell DS&A Exercise

I would split the file into chunks, process using multithreading using generators and hash tables (defaultdict) to count tokens.

## Iteration 1

My first version is to implement the core functional requirement which is replicating the bash script. For now the additional requirements given in notes will be set aside for later versions.

```bash
#!/bin/bash
cat $1 | tr " .,();{}[]" "\n" | sort | grep -v "^$" | uniq -c | sort -nr | head -20
```

Broken down this means:
1. Load the file via file name
2. Replace all non-alphanumeric characters with newlines
3. Sort the lines alphabetically
4. Remove any empty lines
5. Count the unique occurrences of each line (word) and prefix word with count
6. Sort the lines in descending order of count
7. Display the top 20 lines (words) by count

Outcome: 
* Whilst the output looks reasonable, it produces different counts to the same bash file run in the terminal
* We also don't preserve case for 'I'
