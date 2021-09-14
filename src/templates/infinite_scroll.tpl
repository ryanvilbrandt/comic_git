{# This template extends the base.tpl template, meaning that base.tpl provides a large framework
   that this template then adds to. See base.tpl for more information. #}
{% extends "base.tpl" %}
{# This is the start of the `content` block. It's part of the <body> of the page. This is where all the visible
   parts of the website after the links bar and before the "Powered by comic_git" footer go. #}
{% block content %}
    <div id="jump-to">
        {%- if storylines.keys() | list != ["Uncategorized"] %}
        <h2>Jump to...</h2>
        {%- endif %}
        {# For loops let you take a list of a values and do something for each of those values. In this case,
           it runs through list of all the storylines in the comic (Chapter 1, Chapter 2, etc.) it generates a link
           for each of those them connecting to the first page in that storyline. #}
        {%- for name, pages in storylines.items() %}
            {# When text is surrounded by {{ these double curly braces }}, it's representing a variable that's passed in by
               the Python script that generates the HTML file. That value is dropped into the existing HTML with no changes.
               For example, if `pages` is a list of items and the first item has a variable on it called `page_name`,
               and the value of that is `Chapter 3`, then `href="#{{ pages[0].page_name }}"` becomes
               `href="#Chapter 3"` #}
            {%- if name != "Uncategorized" %}
            {# `| replace(" ", "-")` takes the value in the variable, in this case `name`, and replaces all
               spaces with hyphens. This is important when building links to other parts of the site. #}
            <a class="chapter-links" href="#{{ pages[0].page_name }}" id="infinite-scroll-{{ name | replace(' ', '-') }}">{{ name }}</a>
            {%- endif %}
        {%- endfor %}
    </div>
    <div id="load-older" hidden>
        <button id="load-older-button">Load Older</button>
    </div>
    <div id="loading-infinite-scroll"><p>Loading comics...</p></div>
    <div id="infinite-scroll"></div>
    <div id="load-newer">
        <button id="load-newer-button">Load Newer</button>
    </div>
    <div id="caught-up-notification" hidden>
        <h2>You're all caught up!</h2>
    </div>
{% endblock %}
{% block script %}
<script type="module">
    import { load_page } from "{{ base_dir }}/src/js/infinite_scroll.js";
    load_page("{{ comic_base_dir }}", "{{ content_base_dir }}");
</script>
{% endblock %}
