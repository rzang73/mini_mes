SELECT *
  FROM products;

SELECT *
  FROM production_history;

SELECT h.history_id,
       p.name,
       h.qty,
       h.prod_date
  FROM Production_History h
       INNER JOIN
       Products p ON h.product_id = p.product_id;

SELECT product_id,
       sum(qty) 
  FROM production_history
 GROUP BY product_id;

SELECT *
  FROM production_history
 WHERE prod_date = '2026-06-23';

SELECT product_id,
       SUM(qty) 
  FROM production_history
 GROUP BY product_id;

INSERT INTO production_history VALUES (
                                   5,
                                   1,
                                   200,
                                   '2026-06-24'
                               );

INSERT INTO production_history VALUES (
                                   6,
                                   2,
                                   150,
                                   '2026-06-24'
                               );

INSERT INTO production_history VALUES (
                                   7,
                                   3,
                                   90,
                                   '2026-06-24'
                               );

SELECT *
  FROM production_history;

CREATE TABLE production (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    qty INTEGER,
    price INTEGER,
    prod_date TEXT
);

INSERT INTO production VALUES
(1,'Motor',100,5000,'2026-06-22'),
(2,'Sensor',200,12000,'2026-06-22'),
(3,'Pump',150,8000,'2026-06-23'),
(4,'Bearing',80,3000,'2026-06-23'),
(5,'Valve',120,9000,'2026-06-24');

SELECT
product_name,
LENGTH(product_name)
FROM production;
