{# This template extends the base.tpl template, meaning that base.tpl provides a large framework
   that this template then adds to. See base.tpl for more information. #}
{% extends "base.tpl" %}
{# `block head` means that the next two lines go where the `head` block is defined in base.tpl #}
{%- block head %}
    {# `super()` means that everything that's currently in the `head` block in base.tpl is added first, and then the
       next line is added to the end. #}
    {{- super() }}
    <link rel="next" href="{{ base_dir }}/comic/{{ next_id }}/">
{%- endblock %}
{# This is the start of the `content` block. It's part of the <body> of the page. This is where all the visible
   parts of the website after the links bar and before the "Powered by comic_git" footer go. #}
{%- block content %}
    {# When text is surrounded by {{ these double curly braces }}, it's representing a variable that's passed in by
       the Python script that generates the HTML file. That value is dropped into the existing HTML with no changes.
       For example, if the value passed in to `base_dir` is `comic_git`, then `{{ base_dir }}/comic` becomes
       `/comic_git/comic` #}
    <div id="comic-page">
        <a href="{{ base_dir }}/comic/{{ next_id }}/#comic-page">
            <img id="comic-image" src="{{ base_dir }}/{{ comic_path }}" title="{{ alt_text }}"/>
        </a>
    </div>

    {# If blocks let you check the value of a variable and then generate different HTML depending on that variable.
       The if block below will generate non-functioning links for `First` and `Previous` if the current page is the
       first page in the comic, and functioning links otherwise. #}
    <div id="navigation-bar">
    {% if first_id == current_id %}
        <a class="navigation-button-disabled">‹‹ First</a>
        <a class="navigation-button-disabled">‹ Previous</a>
    {% else %}
        <a class="navigation-button" href="{{ base_dir }}/comic/{{ first_id }}/#comic-page">‹‹ First</a>
        <a class="navigation-button" href="{{ base_dir }}/comic/{{ previous_id }}/#comic-page">‹ Previous</a>
    {% endif %}
    {# The block below is the same as the one above, except it checks if you're on the last page. #}
    {% if last_id == current_id %}
        <a class="navigation-button-disabled">Next ›</a>
        <a class="navigation-button-disabled">Last ››</a>
    {% else %}
        <a class="navigation-button" href="{{ base_dir }}/comic/{{ next_id }}/#comic-page">Next ›</a>
        <a class="navigation-button" href="{{ base_dir }}/latest/#comic-page">Last ››</a>
    {% endif %}
    </div>

    <div id="blurb">
        <h1 id="page-title">{{ page_title }}</h1>
        <h3 id="post-date">Posted on: {{ post_date }}</h3>
        {%- if storyline %}
            <div id="storyline">
                {# `| replace(" ", "-")` takes the value in the variable, in this case `storyline`, and replaces all
                   spaces with hyphens. This is important when building links to other parts of the site. #}
                Storyline: <a href="{{ base_dir }}/archive/#{{ storyline | replace(" ", "-") }}">{{ storyline }}</a>
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
                <a href="{{ base_dir }}/tagged/{{ character }}/">{{ character }}</a>{% if not loop.last %}, {% endif %}
            {%- endfor %}
            </div>
        {%- endif %}
        {%- if tags %}
            <div id="tags">
            Tags:
            {%- for tag in tags %}
                <a class="tag-link" href="{{ base_dir }}/tagged/{{ tag }}/">{{ tag }}</a>{% if not loop.last %}, {% endif %}
            {%- endfor %}
            </div>
        {%- endif %}
        <hr id="post-body-break">
        <div id="post-body">
{{ post_html }}
        </div>
        {% if transcripts %}
        <table id="transcripts-container" border>
            <tr>
                <td id="transcript-panel">
                    <h3>Transcript</h3>
                    <div id="active-transcript">
                    {% for language, transcript in transcripts.items() %}
                        <div class="transcript" id='{{ language }}-transcript'>
                        {{ transcript }}
                        </div>
                    {% endfor %}
                    </div>
                </td>
                <td id="language-list">
                    <label for="language-select">Languages</label>
                    <select id="language-select" size="7">
                        {% for language in transcripts.keys() %}
                        <option>{{ language }}</option>
                        {% endfor %}
                    </select>
                </td>
            </tr>
        </table>
        {% endif %}
    </div>
{%- endblock %}
{%- block script %}
{% if transcripts %}
<script type="module">
    import { init } from "{{ base_dir }}/src/js/transcript.js";
    init();
</script>
{% endif %}
{%- endblock %}