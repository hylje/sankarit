INSERT INTO player (id, username, email, password, gold)
VALUES
(1, 'xyz', 'x@yz.yz', 'abc', 0),
(2, 'zyx', 'z@yx.yx', 'abc', 1000);

INSERT INTO hero (id, name, class, xp, player_id)
VALUES
(1, 'Conan', 1, 4000, 1),
(2, 'Legolas', 2, 3000, 1),
(3, 'Thrall', 3, 2000, 1),
(4, 'Sven', 1, 5000, 2);

INSERT INTO adventure (id, start_time, end_time, class, gold)
VALUES
(1, '1999-01-08 04:05:06', '1999-01-08 10:05:06', 1, 100),
(2, '1999-02-08 04:05:06', '1999-02-08 10:05:06', 1, 100);

INSERT INTO adventure_hero (hero_id, adventure_id)
VALUES
(1, 1),
(2, 1),
(4, 2);

INSERT INTO item (id, level, class, slot, rarity,
       	    	  player_id, adventure_id, hero_id)
VALUES
(1, 1, 1, 1, 1, 1, 1, 1),
(2, 2, 2, 1, 1, 1, 1, NULL),
(3, 1, 1, 1, 1, 2, 2, 4),
(4, 3, 3, 1, 1, 2, 2, NULL);
