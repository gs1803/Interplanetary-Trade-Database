USE PLANET_DB;

INSERT INTO Planets (planet_id, planet_name, population_size, economic_development, galaxy_name, galaxy_id) VALUES (31, 'Database Systems', 555555, 4, 'ECSS', 16);

UPDATE Planets
SET planet_name = 'Database Design'
WHERE planet_id = 31;

DELETE FROM Planets
WHERE planet_id = 31;

-- Name of planet with most disputes
SELECT p.planet_name, COUNT(td.dispute_id) AS dispute_count
FROM Planets p
JOIN Trade_Agreements ta ON p.planet_id = ta.participating_planet1
LEFT JOIN Trade_Disputes td ON ta.agreement_id = td.dagreement_id
GROUP BY p.planet_name
ORDER BY dispute_count DESC
LIMIT 1;

-- Find the top 5 planets with the highest quality-rated products and their respective average product prices:
SELECT p.planet_name, AVG(pr.price) AS avg_product_price
FROM Planets p
JOIN Products pr ON p.planet_id = pr.pplanet_id
GROUP BY p.planet_name
ORDER BY MAX(pr.quality_rating) DESC
LIMIT 5;

-- Cost of an occurence using aggregate functions: average distance taken in trade routes
SELECT AVG(t.distance_taken) as avg_distance
FROM Trade_Routes t;

-- Get multiple arrival dates of cargo items from the week of Sept 13 to 20 
SELECT c.cargo_id, c.date_shipped, c.estimated_arrival_date, c.actual_arrival_date
FROM Cargo c
WHERE c.actual_arrival_date >= "2023-09-13" && c.actual_arrival_date <= "2023-09-20"
ORDER BY c.actual_arrival_date;

-- List the planets that have allocated the most money for technology development and their corresponding technology levels:
SELECT p.planet_name, t.tech_level, t.money_allocated
FROM Planets p
JOIN Technology t ON p.planet_id = t.tplanet_id
ORDER BY t.money_allocated DESC;

-- Get total price of shipment
SELECT c.cargo_id, c.quantity_product, c.quantity_raw_material, 
       (c.quantity_product * p.price + c.quantity_raw_material * r.cost_per_unit) AS total_price, 
       c.cagreement_id AS agreement_id, p1.planet_name AS origin_planet_name, 
       p2.planet_name AS destination_planet_name, p.product_id, p.product_name,
       r.raw_material_name FROM Cargo c
JOIN Products p ON c.cproduct_id = p.product_id
JOIN Raw_Materials r ON c.craw_material_id = r.raw_material_id
JOIN Trade_Agreements ta ON c.cagreement_id = ta.agreement_id
JOIN Planets p1 ON ta.participating_planet1 = p1.planet_id
JOIN Planets p2 ON ta.participating_planet2 = p2.planet_id;


SELECT * FROM Planets
LIMIT 1;

SELECT * FROM Trade_Agreements
LIMIT 1;

SELECT * FROM Trade_Routes
LIMIT 1;

SELECT * FROM Trade_Disputes
LIMIT 1;

SELECT * FROM Products
LIMIT 1;

SELECT * FROM Cargo
LIMIT 1;

SELECT * FROM Technology
LIMIT 1;

SELECT * FROM Raw_Materials
LIMIT 1;

 -- DROP DATABASE PLANET_DB;