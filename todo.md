Some things that need to be added/done:

- Config file to change options

  From CBZPlatter.py:
- Put the zipList into a class to keep track of all the stuff I do with it
- Also could put the supportedFileType check in generateHTMLPage into its own def and use that with zipListIndex
- Thirdly thumbs.db keeps showing up and preventing folder from being deleted.
- Need to have more robust error handling
- Maybe a verbose command to print out where things are etc.
- subfolders in zip files cause issues
- If enough files, no thumbnails? just file names? Maybe seperate by folders?
- Add swipe gestures for mobile devices
- Down the road I want minimize thumbnails
- Thumbnails should have correct aspect ratio in index.html
- Support for PDF, EPUB, and RAR even if that requires external packages
- File order in zips are messed up if different file types are contained

  Others:
- Update the logging feature
-<s> Add back support for python 2 with SimpleHTTPServer</s>
- Probably split up the webserver and webpage generator into seperate files
-<s> HTML generation from python package html/html.parser</s>
- Some sort of button on the index page to delete or regenerate all subpages
 - (if a html file is not deleted after previous server it will never be updated)
- Sorting options for files
