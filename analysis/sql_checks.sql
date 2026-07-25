-- SQLite-compatible validation checks for the test/vendor handoff.
SELECT treatment_group, COUNT(*) AS stores FROM test_assignments GROUP BY treatment_group;
SELECT store_id, week, expected_rows, received_rows, null_rate FROM data_feed_validation WHERE received_rows <> expected_rows OR null_rate > 0.005;
SELECT treatment_group, segment, COUNT(*) AS transactions, ROUND(AVG(net_sales),2) AS aov, ROUND(AVG(converted),4) AS conversion_rate FROM transactions GROUP BY treatment_group, segment;
