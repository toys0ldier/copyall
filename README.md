# copyall

This simple script can copy and move files and folders from a source to destination directory. Optionally, you can specify an extension or multiple extensions (seperated by comma's) and the script will only action files matching the extension(s) specified. In testing, this is substantially faster than any GUI-based copy or move operation and also provides a greater granularity of tracking by denoting successes as well as how many items failed to copy and why.

```
Usage: [move/copy] [source] [destination] [extensions (optional)]

Available flags:
copy    ->   copies items from source to destination
move    ->   moves items from source to destination
ext     ->   action only items with specified extension(s)
             supply multiple extensions like: exe,png,jpg

Enclose multi-word searches with single quotes, i.e. 'foo bar'

Created by toys0ldier, github.com/toys0ldier
```