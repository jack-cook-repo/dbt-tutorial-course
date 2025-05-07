<!-- This markdown file is created to created reusable comment block so that it can be use across multiple places and changes are consistent.
We can create this file in model or test or seed folder where dbt run command will look.
You can create table, mentioned comment in bulleted data.
-->
{% docs status %}

The status of the order. Can be one of:
- Processing
- Cancelled
- Shipped
- Complete
- Returned

{% enddocs %}