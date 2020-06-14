{{ autogenerate_warning }}
<!DOCTYPE html>
<html lang="en" prefix="og: http://ogp.me/ns#">
<head>
    {%- block head %}
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="/{{ base_dir }}/src/css/style.css">
    <link rel="stylesheet" type="text/css" href="/{{ base_dir }}/your_content/colors_and_layout/your_stylesheet.css">
    <link rel="icon" href="/{{ base_dir }}/favicon.ico" type="image/x-icon" />
    <meta property="og:title" content="{{ comic_title }}" />
    <meta property="og:description" content="{{ comic_description }}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{{ comic_url }}" />
    <meta property="og:image" content="{{ comic_url + '/your_content/images/preview_image.png' }}" />
    <meta property="og:image:width" content="100px" />
    <meta property="og:image:height" content="100px" />
    <title>{{ page_title }} - {{ comic_title }}</title>
    {%- endblock %}
</head>
<body>
{% block body %}
<div id="container">
    <div id="banner">
        <a id="banner-img-link" href="/{{ base_dir }}/">
            <img id="banner-img" alt="banner" src="/{{ base_dir }}/your_content/images/banner.png">
        </a>
    </div>
    <div id="links-bar">
    {%- for link in links %}
        <a class="link-bar-link" href="{{ link.url }}">{{ link.name }}</a>
    {%- endfor %}
    </div>

    {% block content %}{% endblock %}

    <div id="powered-by">
        Powered by <a id="powered-by-link" href="https://github.com/ryanvilbrandt/comic_git">comic_git</a> v{{ version }}
    </div>
</div>
{% endblock %}
</body>
{% block script %}{% endblock %}
</html>
