"""
Track A / V1 — daily snapshot job (skeleton).
Reads the five orion_sandbox.vw_* late-binding views and writes Parquet to the test bucket,
partitioned year/month/day. Cadence is one-for-one with production (daily).

Configuration comes from Glue job arguments, never from literals in this file (REPRO-1).
Idempotent: re-running a day overwrites that day's partition only (IDEM-1).
Export the real script from Glue → Jobs → Script and replace this skeleton; keep the argument contract.
"""
import sys
from datetime import date
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext

ARGS = getResolvedOptions(sys.argv, [
    "BUCKET", "SNAPSHOT_PREFIX", "GLUE_DATABASE",
    "REDSHIFT_CONNECTION",   # SMUS/Glue connection name; credentials live in Secrets Manager, not here
    "AS_OF",                 # YYYY-MM-DD; default handled below
])

VIEWS = ["vw_Account", "vw_d_Account", "vw_Household", "vw_Registration", "vw_Representative"]

def main():
    sc = SparkContext.getOrCreate()
    glue = GlueContext(sc)
    spark = glue.spark_session
    as_of = ARGS.get("AS_OF") or date.today().isoformat()
    y, m, d = as_of.split("-")

    for view in VIEWS:
        df = glue.create_dynamic_frame.from_options(
            connection_type="redshift",
            connection_options={
                "useConnectionProperties": "true",
                "connectionName": ARGS["REDSHIFT_CONNECTION"],
                "dbtable": f"orion_sandbox.{view}",
            },
        ).toDF()
        target = f"s3://{ARGS['BUCKET']}/{ARGS['SNAPSHOT_PREFIX']}/{view}/year={y}/month={m}/day={d}/"
        # overwrite only this partition -> safe to re-run (IDEM-1)
        df.write.mode("overwrite").parquet(target)
        print(f"snapshot written: {view} -> {target} rows={df.count()}")

if __name__ == "__main__":
    main()
