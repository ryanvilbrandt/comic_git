{% extends "base.tpl" %}
{%- block content %}

    <h1>Welcome to my website!</h1>

    <p>This is the main landing page! Isn't it cool?? This is where I'm pitching my comic to you.</p>

    <p>Checkout the links below to go to the first and last pages of my comic.</p>

    <div id="navigation-bar">
        <a class="navigation-button" href="comic/{{ first_id }}/#comic-page">First</a>
        <a class="navigation-button" href="comic/{{ last_id }}/#comic-page">Last</a>
    </div>

    <p>Checkout the links bar above for links to my shop and patreon and other ways for you to give me money.</p>

{%- endblock %}