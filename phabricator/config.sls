{% from "phabricator/default.yml" import lookup, rawmap with context %}
{% set lookup = salt['grains.filter_by'](lookup, grain='os', merge=salt['pillar.get']('phabricator:lookup')) %}
{% set rawmap = salt['pillar.get']('phabricator', rawmap) %}

{% if rawmap.config is defined and rawmap.config is mapping %}
    {% for item_name, item_config in rawmap.config.items() %}
        {% if item_config is mapping %}
            {% set item_value = item_config.value %}
            {% set item_state = item_config.state|default('managed') %}
        {% else %}
            {% set item_value = item_config %}
            {% set item_state = 'managed' %}
        {% endif %}
{{item_name ~ '_config_option'}}:
    phabricator_config:
        - {{item_state}}
        - name: {{item_name}}
        - value: {{item_value}}
        - bin: {{rawmap.root_dir}}
    {% endfor %}
{% endif %}
