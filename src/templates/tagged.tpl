{% extends "base.tpl" %}
{% block content %}
    <h1 id="page-title">Posts tagged with "{{ tag }}"</h1>

    <div id="blurb">
        <div id="tagged">
            <ul>
            {%- for page in tagged_pages %}
                <li><a href="/{{ base_dir }}/comic/{{ page["page_name"] }}/#comic-page">{{ page["page_title"] }}</a> -- {{ page["post_date"] }}</li>
            {%- endfor %}
            </ul>
        </div>
    </div>
{% endblock %}
