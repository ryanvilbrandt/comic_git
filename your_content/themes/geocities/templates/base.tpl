{{ autogenerate_warning }}
<!DOCTYPE html>
<html lang="en" prefix="og: http://ogp.me/ns#">
<head>
    {%- if google_analytics_id %}
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ google_analytics_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', '{{ google_analytics_id }}');
    </script>
    {%- endif %}
    {%- block head %}
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="{{ base_dir }}/src/css/advanced_stylesheet.css">
    <link rel="stylesheet" type="text/css" href="{{ base_dir }}/your_content/themes/{{ theme }}/css/stylesheet.css">
    <link rel="icon" href="{{ base_dir }}/favicon.ico" type="image/x-icon" />
    <meta property="og:title" content="{{ comic_title }}" />
    <meta property="og:description" content="{{ comic_description }}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{{ comic_url }}/" />
    <meta property="og:image" content="{{ comic_url + '/your_content/images/preview_image.png' }}" />
    <meta property="og:image:width" content="100px" />
    <meta property="og:image:height" content="100px" />
    <title>{{ page_title }} - {{ comic_title }}</title>
    {%- endblock %}
</head>
<body>
{% block body %}
<h1>Welcome to {{ comic_title }}!</h1>

<hr>

<h2>Look at my cool links!</h2>
{%- for link in links %}
    <a href="{{ link.url }}">{{ link.name }}</a>
    {% if not loop.last %}<img src="{{ base_dir }}/your_content/themes/geocities/images/dance.gif" width="50px;">{% endif %}
{%- endfor %}

<hr>

<h2 id="comic-blinker">vvv I MADE A COMIC CHECK IT OUT! vvv</h2>

{% block content %}{% endblock %}

<div id="powered-by">
    Powered by <a id="powered-by-link" href="https://github.com/ryanvilbrandt/comic_git">comic_git</a> v{{ version }}
</div>
{% endblock %}
</body>
{% block script %}{% endblock %}
</html>
