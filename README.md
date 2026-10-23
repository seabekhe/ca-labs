# ca-labs

A small Declarative Automation Bundle used in a hands-on Databricks training session: one Lakeflow Spark Declarative
Pipeline and one Lakeflow Job, deployed into whatever catalog and schema you pass in. All data used in the session is
synthetic.

```
bundle/
  databricks.yml           the pipeline and job, with dev and prod targets
  src/account_summary.sql  the pipeline: a materialized view of accounts by type, operating company, and status
```

## Use it in Databricks (pull only)

1. In your workspace: **Workspace → Create → Git folder**, and paste `https://github.com/seabekhe/ca-labs`.
   Public repository, so no Git credential is needed.
2. Create a branch from the Git folder's branch selector if you want to experiment.
3. The training notebook deploys `bundle/` from your Git folder with the Databricks CLI
   (`bundle validate`, `deploy -t dev`, `run`), passing your catalog, schema, and suffix as variables.

Participants pull from this repository; pushing and pull requests are demonstrated by the instructor.

## The variables

| Variable | Meaning |
|---|---|
| `catalog` | Unity Catalog catalog to deploy into (required) |
| `schema` | Schema to deploy into (required) |
| `suffix` | Your suffix, so objects don't collide with other participants (required) |

Example: `databricks bundle deploy -t dev --var catalog=<catalog> --var schema=<schema> --var suffix=<you>`

## Docs

- [Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
- [Bundle variables](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/variables)
- [Git folders](https://learn.microsoft.com/en-us/azure/databricks/repos/)
- [Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/)
