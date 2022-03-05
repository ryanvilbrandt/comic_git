{# This template extends the base.tpl template, meaning that base.tpl provides a large framework
   that this template then adds to. See base.tpl for more information. #}
{% extends "base.tpl" %}
{# This is the start of the `content` block. It's part of the <body> of the page. This is where all the visible
   parts of the website after the links bar and before the "Powered by comic_git" footer go. #}
{% block content %}
    <h1 id="post-title">Archive</h1>

    <div id="blurb">
    {# If blocks let you check the value of a variable and then generate different HTML depending on that variable.
       The if block below will check the `use_thumbnails` variable. If it's True, the template will generate a grid
       of thumbnail images for each comic in the archive, each linking to the comic page.
       If it's False, the template will generate a simple HTML list of links to each comic in the archive.#}
    {%- if use_thumbnails %}
        {%- for name, pages in storylines.items() %}
        {%- if pages %}
        {# `| replace(" ", "-")` takes the value in the variable, in this case `storyline.name`, and replaces all
           spaces with hyphens. This is important when building links to other parts of the site. #}
        {%- if storylines.keys() | list != ["Uncategorized"] %}
        <a id="{{ name | replace(' ', '-') }}"></a>
        <h2 class="archive-section" id="archive-section-{{ name | replace(' ', '-') }}">{{ name }}</h2>
        {%- endif %}
        <div class="archive-grid">
        {# For loops let you take a list of a values and do something for each of those values. In this case,
           it runs through list of all the pages in a particular storyline (Chapter 1, Chapter 2, etc) and creates
           a tiny thumbnail image with a title and post date, all of which link to that comic page if clicked. #}
        {%- for page in pages %}
            <a href="{{ comic_base_dir }}/comic/{{ page.page_name }}/">
            <div class="archive-thumbnail">
                <div class="archive-thumbnail-page"><img src="{{ base_dir }}/{{ page.thumbnail_path }}"></div>
                <div class="archive-thumbnail-title">{{ page.page_title }}</div>
                <div class="archive-thumbnail-post-date">{{ page.archive_post_date }}</div>
            </div>
            </a>
        {%- endfor %}
        </div>
        {%- endif %}
        {%- endfor %}
    {%- else %}
    <ul>
    {%- for name, pages in storylines.items() %}
        {%- if pages %}
            {%- if storylines.keys() | list != ["Uncategorized"] %}
            <li><a id="{{ name | replace(' ', '-') }}"></a>{{ name }}
            <ul>
            {%- endif %}
            {%- for page in pages %}
                <li><a href="{{ comic_base_dir }}/comic/{{ page.page_name }}/">{{ page.page_title }}</a> -- {{ page.post_date }}</li>
            {%- endfor %}
            {%- if storylines.keys() | list != ["Uncategorized"] %}
            </ul>
            {%- endif %}
        </li>
        {%- endif %}
    {%- endfor %}
    </ul>
    {%- endif %}
    </div>
{% endblock %}
