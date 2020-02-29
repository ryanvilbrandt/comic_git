{% extends "base.tpl" %}
{% block content %}
    <div id="load-older" hidden>
        <button id="load-older-button">Load Older</button>
    </div>
    <div id="infinite-scroll"></div>
    <div id="load-newer">
        <button id="load-newer-button">Load Newer</button>
    </div>
{% endblock %}
{% block script %}
<script type="module">
    import { load_page } from "./src/js/infinite_scroll.js";
    load_page();
</script>
{% endblock %}