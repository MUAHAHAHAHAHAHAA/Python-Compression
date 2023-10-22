
# [Python-Compression](https://github.com/MUAHAHAHAHAHAHAA/Python-Compression "Python-Compression")

## Content
1. [Project](#project)
2. [Example Usage](#example-usage)
3. [Resources](#resources)

## Project
This project uses arithmetic coding together with dynamic markov modelling to compress any binary data with structure

## Example Usage
Using the "wrapper.py" file, files can be compressed and decompressed per command:</br>
Compressing the file "test.txt" with the result being written to "compressed"
> \>> cmp test/test.txt test/compressed

Decompressing the file "compressed" with the result being written to "test_dec.txt"
> \>> dcmp test/compressed test/test_dec.txt

## Resources
Paper about arithmetic coding to compress data
https://www.researchgate.net/publication/2799801_Practical_Implementations_of_Arithmetic_Coding

Paper about data compression using dynamic markov modelling
https://plg.uwaterloo.ca/~gvcormac/manuscripts/dmc.pdf