{% extends "base.tpl" %}
{% block head %}
    <meta charset="UTF-8">
    <meta http-equiv = "refresh" content = "0; url = comic/{{ last_id }}.html" />
    <title>Latest Comic - {{ comic_title }}</title>
{% endblock %}
{% block body %}
    <p>Redirecting to comic/{{ last_id }}.html</p>
{% endblock %}