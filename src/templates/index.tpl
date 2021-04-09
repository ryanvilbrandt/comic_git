{# This template extends the base.tpl template, meaning that base.tpl provides a large framework
   that this template then adds to. See base.tpl for more information. #}
{% extends "base.tpl" %}
{# This is the start of the `content` block. It's part of the <body> of the page. This is where all the visible
   parts of the website after the links bar and before the "Powered by comic_git" footer go. #}
{%- block content %}

    <h1>Welcome to comic_git!</h1>

    <p>What you're seeing is the default website created by comic_git, a static-site generator hosted FOR FREE on GitHub Pages, that YOU can use to publish your own web comic easily and quickly!</p>

    <p>Click <a href="comic/{{ first_id }}/#comic-page">here</a> to go to the first page of the sample comic to see how it looks out-of-the-box.<br>
        You can also click <a href="latest/#comic-page">here</a> to go to the latest page, which will always point to the most recently published comic.</p>

    <p>For instructions on how to use comic_git, check out the <a href="https://github.com/ryanvilbrandt/comic_git/wiki">wiki</a>.<br>
        If you'd like to jump right into creating your own webcomic with comic_git, check out the <a href="https://github.com/ryanvilbrandt/comic_git/wiki/Getting-Started">Getting Started</a> section.</p>

{%- endblock %}
