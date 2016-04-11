# CBZ-Platter
Serving up CBZ files for your web viewing enjoyment

-----
#### Introduction

CBZ-Platter is meant to be a small footprint webserver for displaying CBZ files using only modules in Python's standard library. It is currently in a pre-Alpha state with only basic functionality. 

Currently CBZ-Platter will generate a list of CBZ or Zip archive files (which include images) in the directory it is started in, create an index webpage using the first image from each archive, and start a web server with links to each archive. When the link is clicked the server unpacks the archive and generates a new page that displays the images full screen. Scrolling is disabled but buttons are provided to move to the previous image, next image, or the index. The page uses a lazy image load script to load only the current and next image at the full resolution as it was stored in the archive. Though each archive is only unpacked when it is requested, it will persist until the server is shutdown.

----------

#### Requirements (for running from source) 

* python 3.4 (future versions could provide compatibility with early versions of Python)

----------
#### Running

From the source, run "cbzplatter" from the directory you want to discover media in.
