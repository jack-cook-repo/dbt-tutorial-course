The models folder contains all of the SQL data models used in this project.

# Structure
Staging:
- Where we pull in from our data source (src_ecommerce.yml), and create data models from the ecommerce dataset
- Named in the convention of `stg_{{source_name}}__{{model_name}}`
- Staging models selects from a single source, and are used for basic operations - renaming columns, casting values to datatypes, deduplicating rows etc.

Intermediate:
- Where we combine staging tables, but don't product outputs that you'd want to use for dashboards
- Named in the convention of `int_{{source_name}}__{{model_name}}`
- Intermediate models are where we start to use joins and do more complicated calculations - e.g. joining users table to distribution centers table to calculate distance between users and centers

Marts:
- The "data warehouse"

