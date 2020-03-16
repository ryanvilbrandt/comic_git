{% extends "base.tpl" %}
{% block content %}
    <div id="load-older" hidden>
        <button id="load-older-button">Load Older</button>
    </div>
    <div id="infinite-scroll"></div>
    <div id="load-newer">
        <button id="load-newer-button">Load Newer</button>
    </div>
    <div id="caught-up-notification" hidden>
        <h3>You're all caught up!</h3>
    </div>
{% endblock %}
{% block script %}
<script type="module">
    import { load_page } from "./src/js/infinite_scroll.js";
    load_page();
</script>
{% endblock %}