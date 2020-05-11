<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Style sheet for margins and advanced layout -->
    <link rel="stylesheet" type="text/css" href="/{{ base_dir }}/src/css/style.css">
    <!-- Style sheet for colors and fonts -->
    <link rel="stylesheet" type="text/css" href="/{{ base_dir }}/your_content/colors_and_layout/your_stylesheet.css">
    <title>{{ page_title }} - {{ comic_title }}</title>
</head>
<body>
    <!-- Banner Image -->
    <div id="banner"><img id="banner-img" src="/{{ base_dir }}/your_content/images/banner.png"></div>
    <!-- Links Bar -->
    <div id="links-bar">
    {%- for link in links %}
        <a class="link-bar-link" href="{{ link.url }}">{{ link.name }}</a>
    {%- endfor %}
    </div>

    <!-- Comic Page -->
    <a href="{{ next_id }}.html">
        <img src="/{{ base_dir }}/{{ comic_path }}" title="{{ alt_text }}"/>
    </a>

    <!-- Navigation links. Supports disabling the links when you're at the first or last page. -->
    <div>
        {%- if first_id == current_id %}
            <a>First</a>
            <a>Previous</a>
        {%- else %}
            <a href="{{ first_id }}.html#comic-page">First</a>
            <a href="{{ previous_id }}.html#comic-page">Previous</a>
        {%- endif %}
        {%- if last_id == current_id %}
            <a>Next</a>
            <a>Last</a>
        {%- else %}
            <a href="{{ next_id }}.html#comic-page">Next</a>
            <a href="{{ last_id }}.html#comic-page">Last</a>
        {%- endif %}
    </div>

    <!-- The comic "blurb" at the bottom with title, post date, tags, etc -->
    <h1>{{ page_title }}</h1>
    <div>Posted on: {{ post_date }}</div>

    <!-- The storyline this page is in, with a link to the first page in that storyline -->
    {%- if storyline %}
        <div>Storyline: <a href="/{{ base_dir }}/comic/{{ storyline_id }}.html#comic-page">{{ storyline }}</a></div>
    {%- endif %}

    <!-- List of characters in this comic, with a link to a web page that lists all comics with that character -->
    {%- if characters %}
        <div>
        Characters:
        {%- for character in characters %}
            <!-- "if not loop.last" puts commas after every tag except at the very end -->
            <a href="/{{ base_dir }}/tagged.html?tag={{ character }}">{{ character }}</a>{% if not loop.last %}, {% endif %}
        {%- endfor %}
        </div>
    {%- endif %}

    <!-- List of other tags on this comic, with a link to a web page that lists all comics with that tag -->
    {%- if tags %}
        <div>
        Tags:
        {%- for tag in tags %}
            <!-- "if not loop.last" puts commas after every tag except at the very end -->
            <a href="../tagged.html?tag={{ tag }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
        {%- endfor %}
        </div>
    {%- endif %}

    <hr>
    <!-- The post that goes with this comic -->
    {{ post_html }}
</body>
</html>