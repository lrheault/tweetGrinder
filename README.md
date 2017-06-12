# tweetGrinder
A general Python class to process tweets by category and returning cleaned display text.

Usage:

<code> 
tg = tweetGrinder('desired_output_file.csv')<br>tg.transform('input_streamed_json_file.json')
</code>

Processing a batch of multiple files:

<code> 
for f in sorted(list_of_files):
  tg.transform(f)
</code>
