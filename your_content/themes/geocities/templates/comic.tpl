{% extends "base.tpl" %}
{%- block head %}
    {{- super() }}
    <link rel="next" href="{{ comic_base_dir }}/comic/{{ next_id }}/">
{%- endblock %}
{%- block content %}
    <div id="comic-page">
        <a href="{{ comic_base_dir }}/comic/{{ next_id }}/#comic-page">
            <img id="comic-image" src="{{ base_dir }}/{{ comic_path }}" title="{{ alt_text }}"/>
        </a>
    </div>

    <div id="navigation-bar">
    {% if first_id == current_id %}
        <a class="navigation-button-disabled">‹‹ First</a>
        <a class="navigation-button-disabled">‹ Previous</a>
    {% else %}
        <a class="navigation-button" href="{{ comic_base_dir }}/comic/{{ first_id }}/#comic-page">‹‹ First</a>
        <a class="navigation-button" href="{{ comic_base_dir }}/comic/{{ previous_id }}/#comic-page">‹ Previous</a>
    {% endif %}
    {# The block below is the same as the one above, except it checks if you're on the last page. #}
    {% if last_id == current_id %}
        <a class="navigation-button-disabled">Next ›</a>
        <a class="navigation-button-disabled">Last ››</a>
    {% else %}
        <a class="navigation-button" href="{{ comic_base_dir }}/comic/{{ next_id }}/#comic-page">Next ›</a>
        <a class="navigation-button" href="{{ comic_base_dir }}/latest/#comic-page">Last ››</a>
    {% endif %}
    </div>

    <h1 id="page-title">{{ page_title }}</h1>
    <h3 id="post-date">Posted on: {{ post_date }}</h3>
    {%- if storyline %}
        <div id="storyline">
            {# `| replace(" ", "-")` takes the value in the variable, in this case `storyline`, and replaces all
               spaces with hyphens. This is important when building links to other parts of the site. #}
            Storyline: <a href="{{ comic_base_dir }}/archive/#{{ storyline | replace(' ', '-') }}">{{ storyline }}</a>
        </div>
    {%- endif %}
    {%- if characters %}
        <div id="characters">
        Characters:
        {# For loops let you take a list of a values and do something for each of those values. In this case,
           it runs through list of all the characters in this page, as defined by your info.ini file for this page,
           and it generates a link for each of those characters connecting to the `tagged` page for that
           character. #}
        {%- for character in characters %}
            {# The `if not loop.last` block at the end of the next line means that the ", " string will be added
               after every character link EXCEPT the last one. #}
            <a href="{{ comic_base_dir }}/tagged/{{ character }}/">{{ character }}</a>{% if not loop.last %}, {% endif %}
        {%- endfor %}
        </div>
    {%- endif %}
    {%- if tags %}
        <div id="tags">
        Tags:
        {%- for tag in tags %}
            <a class="tag-link" href="{{ comic_base_dir }}/tagged/{{ tag }}/">{{ tag }}</a>{% if not loop.last %}, {% endif %}
        {%- endfor %}
        </div>
    {%- endif %}
    <hr id="post-body-break">
    <div id="post-body">
{{ post_html|safe }}
    </div>
{%- endblock %}
