{% extends "base.tpl" %}
{% block content %}
    <div id="comic-page">
        <a href="{{ next_id }}.html#comic-page"><img id="comic-image" src="{{ comic_path }}" title="{{ alt_text }}"/></a>
    </div>

    <div id="navigation-bar">
        <table id="navigation-buttons">
            <tr>
                <td id="navigation-button-first">
                    <a class="navigation-button" href="{{ first_id }}.html#comic-page">First</a>
                </td>
                <td id="navigation-button-previous">
                    <a class="navigation-button" href="{{ previous_id }}.html#comic-page">Previous</a>
                </td>
                <td id="navigation-button-next">
                    <a class="navigation-button" href="{{ next_id }}.html#comic-page">Next</a>
                </td>
                <td id="navigation-button-last">
                    <a class="navigation-button" href="{{ last_id }}.html#comic-page">Last</a>
                </td>
            </tr>
        </table>
    </div>

    <div id="blurb">
        <h1 id="page-title">{{ page_title }}</h1>
        <div id="post-date">Posted on: {{ post_date }}</div>
        <div id="tags">
            Tags:
            {% for tag in tags %}
                <a class="tag-link" href="/{{ base_dir }}/tagged.html?tag={{ tag }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
            {% endfor %}
        </div>
        <hr id="post-body-break">
        <div id="post-body">
            {{ post_html }}
        </div>
    </div>
{% endblock %}