{% extends "base.tpl" %}
{%- block head %}
    {{- super() }}
    <link rel="next" href="/{{ base_dir }}/comic/{{ next_id }}.html">
{%- endblock %}
{%- block content %}
    <div id="comic-page">
        <a href="/{{ base_dir }}/comic/{{ next_id }}.html#comic-page">
            <img id="comic-image" src="/{{ base_dir }}/{{ comic_path }}" title="{{ alt_text }}"/>
        </a>
    </div>

    <div id="navigation-bar">
    {% if first_id == current_id %}
        <a class="navigation-button-disabled">First</a>
        <a class="navigation-button-disabled">Previous</a>
    {% else %}
        <a class="navigation-button" href="/{{ base_dir }}/comic/{{ first_id }}.html#comic-page">First</a>
        <a class="navigation-button" href="/{{ base_dir }}/comic/{{ previous_id }}.html#comic-page">Previous</a>
    {% endif %}
    {% if last_id == current_id %}
        <a class="navigation-button-disabled">Next</a>
        <a class="navigation-button-disabled">Last</a>
    {% else %}
        <a class="navigation-button" href="/{{ base_dir }}/comic/{{ next_id }}.html#comic-page">Next</a>
        <a class="navigation-button" href="/{{ base_dir }}/latest.html#comic-page">Last</a>
    {% endif %}
    </div>

    <div id="blurb">
        <h1 id="page-title">{{ page_title }}</h1>
        <h3 id="post-date">Posted on: {{ post_date }}</h3>
        {%- if storyline %}
            <div id="storyline">
                Storyline: <a href="/{{ base_dir }}/comic/{{ storyline_id }}.html#comic-page">{{ storyline }}</a>
            </div>
        {%- endif %}
        {%- if characters %}
            <div id="characters">
            Characters:
            {%- for character in characters %}
                <a href="/{{ base_dir }}/tagged.html?tag={{ character }}">{{ character }}</a>{% if not loop.last %}, {% endif %}
            {%- endfor %}
            </div>
        {%- endif %}
        {%- if tags %}
            <div id="tags">
            Tags:
            {%- for tag in tags %}
                <a class="tag-link" href="../tagged.html?tag={{ tag }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
            {%- endfor %}
            </div>
        {%- endif %}
        <hr id="post-body-break">
        <div id="post-body">
{{ post_html }}
        </div>
    </div>
{%- endblock %}