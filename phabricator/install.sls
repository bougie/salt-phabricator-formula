{% from "phabricator/default.yml" import lookup, rawmap with context %}
{% set lookup = salt['grains.filter_by'](lookup, grain='os', merge=salt['pillar.get']('phabricator:lookup')) %}
{% set rawmap = salt['pillar.get']('phabricator', rawmap) %}

home_directory:
    file:
        - directory
        - name: {{rawmap.root_dir}}
        - makedirs: true

git_package:
    pkg:
        - installed
        - name: {{lookup.git_package}}

{% for repo in ['libphutil', 'arcanist', 'phabricator'] %}
{{repo ~ '_repo'}}:
    git:
        - latest
        - name: {{'https://github.com/phacility/' ~ repo ~ '.git'}}
        - target: {{rawmap.root_dir ~ '/' ~ repo}}
        - require:
            - pkg: git_package
            - file: home_directory
{% endfor %}
