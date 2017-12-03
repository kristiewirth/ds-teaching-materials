* SQL command ordering (i.e., how you must write your queries)

SELECT
FROM
JOIN
ON
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
;

* SQL command execution order (what happens on the back end)
  1 - FROM
  2 - WHERE
  3 - GROUP BY
  4 - HAVING
  5 - SELECT
  6 - DISTINCT
  7 - ORDER
  8 - LIMIT
* SQL style guide -- follow these!! www.sqlstyle.guide
* Every non-aggregated field that is listed in the SELECT list must be listed in the GROUP BY list
* WHERE vs HAVING
  * A WHERE clause is used is filter records from a result.  The filter occurs before any groupings are made
  * A HAVING clause is used to filter values from a group
  * The WHERE clause is applied first, then the results grouped, and finally the groups filtered according to the HAVING clause
* Order by
  * Default = ascending order
  * Add 'DESC' after column name(s)
* Distinct syntax
  * SELECT DISTINCT – everything is distinct
  * COUNT (DISTINCT variable)
* Examples of aggregate functions
  * AVG
  * COUNT
  * FIRST
  * LAST
  * MAX
  * MIN
  * ROUND
  * SUM
  * STRING_AGG(name,  ',')
* Join syntax
  * (INNER) JOIN
  * LEFT JOIN
  * RIGHT JOIN
  * FULL JOIN
* Joining three tables
  * Join two tables first, check the query works, then add another line of joining to join the third table
* Syntax Error Checklist
  * All keywords are spelled correctly
  * All keywords are in the correct order
  * Aliases do not have keywords or reserved words in them. You can use these websites to lookup whether your alias is a keyword or a reserved word:
    * http://hsqldb.org/doc/guide/lists-app.html
    * https://www.petefreitag.com/tools/sql_reserved_words_checker/
    * http://tunweb.teradata.ws/tunstudent/reservedwords.htm
  * Aliases and title names do not contain white spaces (unless the full title is encased in quotation marks)
  * Quotation marks are of the correct type
  * Semi-colons are at the end of your query, not in the middle
  * All opening parentheses are matched with a closing parentheses
  * There are commas between all the items in a list- there is NOT a comma after the last item in a list
  * All text strings are enclosed with the appropriate types of quotation marks
  * Each column name is linked with the correct table name
  * All the necessary join conditions are included for each join
* Use COUNT( * ) to count number of rows total
  * Add a GROUP BY clause to see the number of rows per ID, state, etc.
* Temp tables are generally better than subqueries
  * Temp table syntax:

WITH temptable1 AS
  (SELECT variable1
  FROM table),

WITH temptable2 AS
  (SELECT variable2
  FROM table)

SELECT temptable1.variable1, temptable2.variable2
FROM temptable1
  JOIN temptable2
  ON temptable1.sender = temptable2.recipient AND temptable1.recipient = temptable2.sender;
