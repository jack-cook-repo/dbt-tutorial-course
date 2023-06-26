There are 2 types of test you can create:
1. Generic tests:
	- Can be used in a YML file
	- These must live in either the `macros/` folder or `tests/generic`. I prefer the latter
	- Need to be wrapped in {% test test_name(arguments) %} {% endtest %} within a SQL file
2. Custom tests:
	- Standalone SQL files that live in the `tests/` folder
	- These don't need any {% test %} tags, they just need to use ref('') to point at the model(s) to test

Note that in dbt_project.yml you can specify other paths for your tests under "test-paths"


