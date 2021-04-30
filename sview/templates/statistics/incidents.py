{%- from "_snippets.html" import data_box with context -%}
{%- from "_snippets.html" import pair_data_box with context -%}
{%- from "_snippets.html" import map_box with context -%}
{%- from "_snippets.html" import line_box with context -%}
{%- from "_snippets.html" import country_code_item with context -%}
{%- from "_snippets.html" import big_period_buttons with context -%}
{%- from "_snippets.html" import request_missing_resources with context -%}
{% extends "layout.html" %}
{% block body %}
<div class="row">
	<div class="col-lg-12 pb-3" align="center">
		{{ map_box("map_scores", "Most evil countries", resources["map_scores"]) }}
	</div>
</div>
<div class="row">
	{{ big_period_buttons(resource_names, periods, active_params) }}
</div>
<div class="row">
	<div class="col">
		{{ line_box("all_incidents_graph", "All the recorded incidents during the time", resources["all_incidents_graph"], "day", "count", "Incidents") }}
	</div>
</div>
<div class="row">
	<div class="col-md">
		{% call(data_item) data_box("top_countries", "Most evil countries", resources["top_countries"], "country") -%}
			{{ country_code_item(data_item) }}
		{%- endcall %}
	</div>
	<div class="col-md">
		{% call(data_item) data_box("top_passwords", "Top passwords", resources["top_passwords"], "password") %}
			<a href="{{ url_for("statistics.password_details", encoded_password=data_item|b64) }}">
				{{ data_item }}
			</a>
		{% endcall %}
	</div>
</div>
{{ request_missing_resources(resource_names, resources, active_params) }}
{% endblock %}
