{#
This template extends the comic.tpl template without making any changes to it, which is the same as just doing
   the exact same thing the comic.tpl template does. This is useful when you want one page to duplicate the
   functionality of another page. In the case of index.tpl, it lets the main landing page for the website be the
   same as the comic page for the latest page that's been uploaded.
The reason it will become the latest comic page and not any other page is that the Python script that generates
    the HTML files from these templates passes only the information for the latest comic page into this file.
    See comic.tpl for a better idea about what values are passed in and how it's built.
If you want the main landing page for your website to look different, this is the file you'll want to edit.
   You can follow the examples of other templates and let the Python script provide values to you (like links to
   the first and last pages of the comic), or you can delete everything and write it in pure HTML. comic_git doesn't
   care!
#}
{% extends "comic.tpl" %}