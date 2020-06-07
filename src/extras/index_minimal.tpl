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
<div id="container">
    <!-- Banner Image -->
    <div id="banner"><img id="banner-img" src="/{{ base_dir }}/your_content/images/banner.png"></div>

    <!-- First and lage pages -->
    <div id="navigation-bar">
        <a class="navigation-button" href="comic/{{ first_id }}.html#comic-page">First</a>
        <a class="navigation-button" href="comic/{{ last_id }}.html#comic-page">Last</a>
    </div>

    <!-- Links Bar -->
    <div id="links-bar">
    {%- for link in links %}
        <a class="link-bar-link" href="{{ link.url }}">{{ link.name }}</a>
    {%- endfor %}
    </div>

    <h1>Welcome to my website!</h1>

    <p>This is the main landing page! Isn't it cool?? This is where I'm pitching my comic to you.</p>

    <p>Checkout the navigation links below the header to go to the first and last pages of my comic.</p>

    <p>Checkout the links bar above for links to my shop and patreon and other ways for you to give me money.</p>

    <div id="powered-by">
        Powered by <a id="powered-by-link" href="https://github.com/ryanvilbrandt/comic_git">comic_git</a> v{{ version }}
    </div>
</div>
</body>
</html>