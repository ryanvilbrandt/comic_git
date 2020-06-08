{% extends "base.tpl" %}
{% block content %}
    <h1 id="page-title">Archive</h1>

    <div id="blurb">
    {%- if use_thumbnails %}
        {%- for storyline in storylines %}
        {%- if storyline.pages %}
        <h2 class="archive-section" id="archive-section-{{ storyline.name | replace(' ', '-') }}">{{ storyline.name }}</h2>
        <div class="archive-grid">
        {%- for page in storyline.pages %}
            <a href="/{{ base_dir }}/comic/{{ page.page_name }}.html">
            <div class="archive-thumbnail">
                <div class="archive-thumbnail-page"><img src="/{{ base_dir }}/{{ page.thumbnail_path }}"></div>
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
    {%- for storyline in storylines %}
        {%- if storyline.pages %}
        <li>{{ storyline.name }}
            <ul>
            {%- for page in storyline.pages %}
                <li><a href="/{{ base_dir }}/comic/{{ page.page_name }}.html">{{ page.page_title }}</a> -- {{ page.post_date }}</li>
            {%- endfor %}
            </ul>
        </li>
        {%- endif %}
    {%- endfor %}
    </ul>
    {%- endif %}
    </div>
{% endblock %}