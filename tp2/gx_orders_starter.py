"""CTP 2 - Exercise 3 STARTER: build an expectation suite for ShopFast orders (GX Core 1.x).
Run from the 02_CTP2 folder:  python gx_orders_starter.py
"""
import pandas as pd
import great_expectations as gx

KIT = "../shopfast-kit/data/"   # adapt if your kit is elsewhere
orders = pd.read_csv(KIT + "orders.csv", dtype=str)
customers = pd.read_csv(KIT + "customers.csv", dtype=str)
orders["total_amount_eur"] = pd.to_numeric(orders["total_amount_eur"], errors="coerce")
orders["order_date_dt"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")  # typed copy for range checks
print(orders["channel"].value_counts(), orders["shipping_country"].value_counts())
context = gx.get_context(mode="file")                       # creates ./gx/ (config + Data Docs)
source = context.data_sources.add_or_update_pandas("shopfast")
asset = source.add_dataframe_asset(name="orders")
batch_def = asset.add_batch_definition_whole_dataframe("all_orders")

suite = context.suites.add_or_update(gx.ExpectationSuite(name="orders_suite"))
E = gx.expectations
for e in [
    E.ExpectTableRowCountToBeBetween(min_value=1000, max_value=100000),
    E.ExpectColumnValuesToNotBeNull(column="order_id"),
    E.ExpectColumnValuesToBeUnique(column="order_id"),
    # TODO 1: customer_id must not be null
    E.ExpectColumnValuesToNotBeNull(column="customer_id"),
    # TODO 2: customer_id must exist in customers (hint: ExpectColumnValuesToBeInSet with set(customers["customer_id"]))
    E.ExpectColumnValuesToBeInSet(column="customer_id",value_set=set(customers["customer_id"])),
    # TODO 3: order_date must not be null and must look like YYYY-MM-DD (ExpectColumnValuesToMatchRegex)
    E.ExpectColumnValuesToMatchRegex(column="order_date",regex=r"\d{4}-\d{2}-\d{2}"),
    # TODO 4: no order in the future (ExpectColumnValuesToBeBetween on column "order_date_dt")
    E.ExpectColumnValuesToBeBetween(column="order_date_dt",max_value=pd.Timestamp.today()),
    # TODO 5: status only in: pending, shipped, delivered, cancelled, returned
    E.ExpectColumnValuesToBeInSet(column="status",value_set=["pending", "shipped", "delivered", "cancelled", "returned"],),
    # TODO 6: channel and shipping_country only in their allowed values (look at the data first!)
    E.ExpectColumnValuesToBeInSet(column="channel",value_set=["web", "mobile_app", "marketplace"],),
    E.ExpectColumnValuesToBeInSet(column="shipping_country",value_set=["FR", "DE", "ES", "BE"]),
    # TODO 7: total_amount_eur strictly positive and below a sensible maximum
    E.ExpectColumnValuesToBeBetween(column="total_amount_eur",min_value=0,max_value=10000,strict_min=True)
]:
    suite.add_expectation(e)
suite.save()

vd = context.validation_definitions.add_or_update(gx.ValidationDefinition(name="orders_validation", data=batch_def, suite=suite))
checkpoint = context.checkpoints.add_or_update(gx.Checkpoint(name="orders_checkpoint", validation_definitions=[vd],
                                                             actions=[gx.checkpoint.UpdateDataDocsAction(name="docs")]))
result = checkpoint.run(batch_parameters={"dataframe": orders})

print("\nSuite passed:", result.success)
for vr in result.run_results.values():
    for r in vr.results:
        cfg = r.expectation_config
        print(f"{'PASS' if r.success else 'FAIL'}  {cfg.type:<45} {cfg.kwargs.get('column', ''):<18} unexpected={r.result.get('unexpected_count', '-')}")
print("\nOpen the report: gx/uncommitted/data_docs/local_site/index.html")
