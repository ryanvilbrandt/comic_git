{% extends "base.tpl" %}
{% block content %}
    <h1 id="page-title">Archive</h1>

    <div id="blurb">
        <ul>
        {% for section in archive_sections %}
            <li>{{ section.name }}
                <ul>
                {% for page in section.pages %}
                    <li><a href="/{{ base_dir }}/comic/{{ page.page_name }}.html">{{ page.page_title }}</a> -- {{ page.post_date }}</li>
                {% endfor %}
                </ul>
            </li>
        {% endfor %}
        </ul>
    </div>
{% endblock %}