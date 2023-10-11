-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports;

SELECT description FROM crime_scene_reports WHERE year=2020 AND month=7 AND day=28 AND street="Chamberlin";

SELECT month FROM crime_scene_reports;

SELECT DISTINCT month FROM crime_scene_reports;

SELECT DISTINCT day FROM crime_scene_reports;

SELECT DISTINCT year FROM crime_scene_reports;

SELECT DISTINCT street FROM crime_scene_reports;

SELECT description FROM crime_scene_reports WHERE year=2020 AND month=7 AND day=28 AND street LIKE "%Chamberlin%";

SELECT DISTINCT name, day, month FROM interviews;

SELECT DISTINCT name, day, month, year FROM interviews;

SELECT name, day, month, transcript FROM interviews WHERE month>=7 AND day>=28 AND transcript LIKE "%courthouse%";

--Ruth's lead:
SELECT DISTINCT year FROM courthouse_security_logs;

SELECT day, month, hour, minute, activity, license_plate FROM courthouse_security_logs WHERE month=7 AND day=28 AND hour=10 AND minute>=15;

SELECT day, month, hour, minute, activity, license_plate FROM courthouse_security_logs WHERE month=7 AND day=28 AND hour=10 AND minute>=15 AND activity="exit";

SELECT day, month, hour, minute, activity, license_plate FROM courthouse_security_logs
WHERE month=7 AND day=28 AND hour=10 AND minute>=15 AND minute<=25 AND activity="exit";

SELECT name FROM people WHERE license_plate IN(
SELECT license_plate FROM courthouse_security_logs
WHERE month=7 AND day=28 AND hour=10 AND minute>=15 AND minute<=25 AND activity="exit");

--Eugene's lead:
SELECT atm_location FROM atm_transactions WHERE atm_location LIKE "%Fifer%";

SELECT transaction_type FROM atm_transactions WHERE atm_location LIKE "%Fifer%" AND month=7 AND day=28;

SELECT transaction_type, amount FROM atm_transactions WHERE atm_location LIKE "%Fifer%" AND month=7 AND day=28;

--Raymond's lead:
SELECT duration FROM phone_calls WHERE month=7 AND day=28;

SELECT duration FROM phone_calls WHERE month=7 AND day=28 AND duration<=60;

SELECT day, month, year, caller, receiver, duration FROM phone_calls WHERE month=7 AND day=28 AND duration<=60;

SELECT DISTINCT name FROM people
WHERE phone_number IN(
SELECT caller FROM phone_calls WHERE month=7 AND day=28 AND duration<=60)
OR
phone_number IN(
SELECT receiver FROM phone_calls WHERE month=7 AND day=28 AND duration<=60);

SELECT * FROM flights;

SELECT * FROM flights WHERE month=7 AND day=29 ORDER BY hour, minute;

SELECT * FROM airports WHERE id=8;

SELECT * FROM airports WHERE id=4;

--data crossing
--thief
--phone
SELECT DISTINCT name FROM people
WHERE phone_number IN(
SELECT caller FROM phone_calls WHERE month=7 AND day=28 AND duration<=60);

--atm
SELECT DISTINCT name FROM people WHERE id IN(
SELECT person_id FROM bank_accounts WHERE account_number IN(
SELECT account_number FROM atm_transactions
WHERE atm_location LIKE "%Fifer%" AND month=7 AND day=28 AND transaction_type="withdraw"));

--flight
SELECT DISTINCT name FROM people WHERE passport_number IN(
SELECT passport_number FROM passengers WHERE flight_id IN(
SELECT id FROM flights
WHERE month=7
AND day=29
AND hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29)
AND minute IN(SELECT MIN(minute) FROM flights WHERE hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29) AND month=7 AND day=29)));

--sum
SELECT DISTINCT name FROM people WHERE name IN(
SELECT DISTINCT name FROM people
WHERE phone_number IN(
SELECT caller FROM phone_calls WHERE month=7 AND day=28 AND duration<=60))
AND
name IN(
SELECT DISTINCT name FROM people WHERE id IN(
SELECT person_id FROM bank_accounts WHERE account_number IN(
SELECT account_number FROM atm_transactions
WHERE atm_location LIKE "%Fifer%" AND month=7 AND day=28 AND transaction_type="withdraw")))
AND
name IN(
SELECT DISTINCT name FROM people WHERE passport_number IN(
SELECT passport_number FROM passengers WHERE flight_id IN(
SELECT id FROM flights
WHERE month=7
AND day=29
AND hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29)
AND minute IN(SELECT MIN(minute) FROM flights WHERE hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29) AND month=7 AND day=29))));

SELECT name FROM people WHERE phone_number IN(
SELECT receiver FROM phone_calls
WHERE month=7 AND day=28 AND duration<=60 AND caller IN(
SELECT phone_number FROM people
WHERE name="Bobby"));

SELECT name FROM people WHERE phone_number IN(
SELECT receiver FROM phone_calls
WHERE month=7 AND day=28 AND duration<=60 AND caller IN(
SELECT phone_number FROM people
WHERE name="Madison"));

SELECT name FROM people WHERE phone_number IN(
SELECT receiver FROM phone_calls
WHERE month=7 AND day=28 AND duration<=60 AND caller IN(
SELECT phone_number FROM people
WHERE name="Ernest"));

SELECT DISTINCT name FROM people WHERE name IN(
SELECT DISTINCT name FROM people
WHERE phone_number IN(
SELECT caller FROM phone_calls WHERE month=7 AND day=28 AND duration<=60))
AND
name IN(
SELECT DISTINCT name FROM people WHERE id IN(
SELECT person_id FROM bank_accounts WHERE account_number IN(
SELECT account_number FROM atm_transactions
WHERE atm_location LIKE "%Fifer%" AND month=7 AND day=28 AND transaction_type="withdraw")))
AND
name IN(
SELECT DISTINCT name FROM people WHERE passport_number IN(
SELECT passport_number FROM passengers WHERE flight_id IN(
SELECT id FROM flights
WHERE month=7
AND day=29
AND hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29)
AND minute IN(SELECT MIN(minute) FROM flights WHERE hour IN(SELECT MIN(hour) FROM flights WHERE month=7 AND day=29) AND month=7 AND day=29))))
AND name IN(
SELECT name FROM people WHERE license_plate IN(
SELECT license_plate FROM courthouse_security_logs
WHERE month=7 AND day=28 AND hour=10 AND minute>=15 AND minute<=25 AND activity="exit"));