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

Time & Space complexity:
Merge Sort: O(nlogn) (divide is O(logn) and sort is O(n))
We then loop through and count consecutive lines which is O(n)
Therefore total complexity is O(2logn)

## Iteration 2

Improvements:
* I want to increase the ability to handle large files (we should read line-by-line)
* Improve the efficiency of sorting
* Handle binary files

I read this StackOverflow article on heuristics around [number of hash buckets](https://stackoverflow.com/questions/225621/how-many-hash-buckets)

We use a min heap to maintain the 20 most common elements