{% extends "base.tpl" %}
{% block content %}
    <h1 id="page-title">Archive</h1>

    <div id="blurb">
    {%- if use_thumbnails %}
        {%- for section in archive_sections %}
        {%- if section.pages %}
        <h2 class="archive-section">{{ section.name }}</h2>
        <div class="archive-grid">
        {%- for page in section.pages %}
            <a href="/{{ base_dir }}/comic/{{ page.page_name }}.html">
            <div class="archive-thumbnail">
                <div class="archive-thumbnail-page"><img src="/{{ base_dir }}/{{ page.thumbnail_path }}"></div>
                <div class="archive-thumbnail-title">{{ page.page_title }}</div>
                <div class="archive-thumbnail-post-date">{{ page.post_date }}</div>
            </div>
            </a>
        {%- endfor %}
        </div>
        {%- endif %}
        {%- endfor %}
    {%- else %}
    <ul>
    {%- for section in archive_sections %}
        {%- if section.pages %}
        <li>{{ section.name }}
            <ul>
            {%- for page in section.pages %}
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