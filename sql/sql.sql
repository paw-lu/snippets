-- Joining on OR condition
-- https://stackoverflow.com/questions/19725014/sql-server-left-join-with-or-operator
-- OR seems to be pretty slow, use UNION instead
-- do not do
FROM
    table_a AS a 
    INNER JOIN table_b AS b ON a.id = b.id1
    OR a.id = b.id2
-- do instead
FROM
    table_a AS a
    INNER JOIN table b ON a.id = b.id2
