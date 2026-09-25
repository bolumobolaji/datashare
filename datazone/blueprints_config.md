# DataZone / SMUS domain `${DOMAIN_ID}` — blueprint state (V1)

Role tags (`Enable…Permissions`) do **not** retroactively disable blueprints. Disable by hand
in the DataZone console → domain → Blueprints (both pages).

| Blueprint                                        | V1 state  | Note                                                        |
|--------------------------------------------------|-----------|-------------------------------------------------------------|
| Tooling                                          | Enabled   | Required — creates roles, security groups, Athena workgroups |
| LakeHouseDatabase                                | Enabled   | Glue catalog / ETL                                          |
| LakehouseCatalog                                 | Enabled   | S3 + existing Redshift connections (datashare path)         |
| EmrOnEc2 / EmrOnEks / EmrServerless              | Disabled  | No Spark in Track A                                          |
| PartnerApps / Workflows                          | Disabled  |                                                             |
| RedshiftServerless                               | Disabled  | Re-enable only if a new workgroup must be created in SMUS   |
| QuickSight                                       | Disabled  | Already off                                                  |
| AmazonBedrockGenerativeAI / MLExperiments / MLflowApp | **Reconcile** | Approval sheet lists these off; left enabled in first pass |

Domain: IAM-based, `${REGION}`. "Make your data discoverable": unchecked.
