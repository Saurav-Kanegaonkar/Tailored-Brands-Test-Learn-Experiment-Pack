# Project discovery brief

## JD pain point and stakeholder workflow
An Enterprise Analytics analyst must convert a merchandising or customer offer question into a defensible retail test, coordinate source attributes with IT and a Test & Learn vendor, and make a scale/revise/stop recommendation. Leaders need a clear answer; Analytics needs method consistency; IT and the vendor need a validated feed contract.

## Decision supported
Whether a targeted offer should expand, be revised by segment, or stop after an eight-week matched-store test. Incremental transaction value is primary; margin, conversion, assignment integrity, and feed completeness are guardrails.

## Data-generating process and assumptions
Public transaction-level test data with customer, store, assignment, and feed-quality fields are not appropriate or sufficiently specific. This pack uses deterministic synthetic source-style tables: 8 stores × 8 weeks × 160 transactions, 200 customers, assignment records, and feed-health records. One feed exception is deliberately inserted to demonstrate a decision gate.

## Alternatives considered
A generic dashboard was rejected because the differentiator is experiment design, data-feed validation, and qualified recommendations—not passive KPI monitoring. A web app was rejected because a reproducible evidence pack with SQL checks, source tables, and readout artifacts is more inspectable for this workflow.
