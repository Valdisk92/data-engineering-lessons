/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...
SELECT category.name     as category_name,
       count(fc.film_id) as films_count
FROM category
         LEFT JOIN public.film_category fc on category.category_id = fc.category_id
GROUP BY category.name
ORDER BY films_count DESC;

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
-- SQL code goes here...
SELECT a.last_name, COUNT(r.rental_id) AS rental_count
FROM actor a
         LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
         LEFT JOIN film f ON fa.film_id = f.film_id
         LEFT JOIN inventory inv ON f.film_id = inv.film_id
         LEFT JOIN rental r ON inv.inventory_id = r.inventory_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY rental_count DESC
LIMIT 10;

/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...
WITH payments_by_categories AS (SELECT c.name AS category_name, SUM(p.amount) AS sum_payments
                                FROM category c
                                         JOIN film_category fc ON c.category_id = fc.category_id
                                         JOIN inventory i ON i.film_id = fc.film_id
                                         JOIN rental r ON r.inventory_id = i.inventory_id
                                         JOIN payment p ON p.rental_id = r.rental_id
                                GROUP BY c.name),
     max_payment AS (SELECT MAX(sum_payments) AS max_sum_payments
                     FROM payments_by_categories)
SELECT category_name, sum_payments
FROM payments_by_categories
         JOIN max_payment ON payments_by_categories.sum_payments = max_payment.max_sum_payments;


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...
SELECT f.title
FROM film f
         LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.film_id IS NULL;

-- OR
SELECT f.title
FROM film f
WHERE NOT EXISTS (SELECT 1
                  FROM inventory i
                  WHERE i.film_id = f.film_id);


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
SELECT a.first_name, a.last_name, COUNT(f.film_id) AS film_count
FROM actor a
         JOIN film_actor fa ON a.actor_id = fa.actor_id
         JOIN film f ON fa.film_id = f.film_id
         JOIN film_category fc ON f.film_id = fc.film_id
         JOIN category c ON fc.category_id = c.category_id
WHERE c.name = 'Children'
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY film_count DESC
LIMIT 3;

