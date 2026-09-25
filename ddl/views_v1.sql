-- Track A / V1 — consumer late-binding views over the Orion datashare.
-- One-for-one against production. Schema shape verified by DS-3; values by V1-5.
-- A datashare consumer can only create late-binding views over shared objects.
-- Replace <shared_db> with the local database created FROM DATASHARE.

CREATE SCHEMA IF NOT EXISTS orion_sandbox;

CREATE OR REPLACE VIEW orion_sandbox.vw_Account          AS SELECT * FROM <shared_db>.<schema>.vw_Account          WITH NO SCHEMA BINDING;
CREATE OR REPLACE VIEW orion_sandbox.vw_d_Account        AS SELECT * FROM <shared_db>.<schema>.vw_d_Account        WITH NO SCHEMA BINDING;
CREATE OR REPLACE VIEW orion_sandbox.vw_Household        AS SELECT * FROM <shared_db>.<schema>.vw_Household        WITH NO SCHEMA BINDING;
CREATE OR REPLACE VIEW orion_sandbox.vw_Registration     AS SELECT * FROM <shared_db>.<schema>.vw_Registration     WITH NO SCHEMA BINDING;
CREATE OR REPLACE VIEW orion_sandbox.vw_Representative   AS SELECT * FROM <shared_db>.<schema>.vw_Representative   WITH NO SCHEMA BINDING;

-- TODO (DS-3): replace SELECT * with the explicit production column list once the
-- prod view definitions are exported, so DDL parity is exact rather than inherited.
