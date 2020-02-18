{% extends "base.tpl" %}
{% block content %}
    <h1 id="page-title">&nbsp;</h1>

    <div id="blurb">
        <div id="tagged">Loading tags...</div>
    </div>
{% endblock %}
{% block script %}
<script type="module">
    import { load_page } from "./src/js/tagged.js";
    load_page();
</script>
{% endblock %}