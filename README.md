# tweetGrinder
A general Python class to process tweets by type and returning the cleaned display text and other metadata.  Contains an English filter.

Usage:

```python
tg = tweetGrinder('desired_output_file.csv')
tg.transform('input_streamed_json_file.json')
```

Processing a batch of multiple files:

```python 
list_of_files = ['path/file1.json', 'path/file2.json', 'path/file3.json']
for f in sorted(list_of_files):
  tg.transform(f)
```
Output:

The output csv file contains the following default columns: 
<ol>
<li> ID number </li>
<li> Date </li>
<li> User handle </li>
<li> Type (extended, retweet, quote, ...) </li>
<li> Raw text </li>
<li> Display text (the text as it appears on Twitter) </li>
<li> Original URL </li>
<li> Quoted text (the text being quoted, if a quote) </li>
</ol>
