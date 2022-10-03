CREATE TABLE IF NOT EXISTS public."Checkins"
(
    "ID" integer NOT NULL,
    "Session_ID" integer NOT NULL,
    "Player_ID" integer NOT NULL,
    CONSTRAINT "Checkins_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Clans"
(
    "ID" integer NOT NULL,
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Clans_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Players"
(
    "ID" integer NOT NULL,
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Clan_ID" integer NOT NULL,
    CONSTRAINT "Players_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Points"
(
    "ID" integer NOT NULL,
    "Player_ID" integer NOT NULL,
    "Season_ID" integer NOT NULL,
    "Points" integer NOT NULL DEFAULT 0,
    "Clan_ID" integer NOT NULL,
    CONSTRAINT "Points_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Seasons"
(
    "ID" integer NOT NULL,
    "Start_Date" date NOT NULL,
    "End_Date" date,
    CONSTRAINT "Seasons_pkey" PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS public."Sessions"
(
    "ID" integer NOT NULL,
    "Start_Time" date NOT NULL,
    "End_Time" date,
    "Season_ID" integer NOT NULL,
    CONSTRAINT "Sessions_pkey" PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Checkins"
    ADD CONSTRAINT player_id FOREIGN KEY ("Player_ID")
    REFERENCES public."Players" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Checkins"
    ADD CONSTRAINT session_id FOREIGN KEY ("Session_ID")
    REFERENCES public."Sessions" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Players"
    ADD CONSTRAINT clan_id FOREIGN KEY ("Clan_ID")
    REFERENCES public."Clans" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Points"
    ADD CONSTRAINT clan_id FOREIGN KEY ("Clan_ID")
    REFERENCES public."Clans" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Points"
    ADD CONSTRAINT player_id FOREIGN KEY ("Player_ID")
    REFERENCES public."Players" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Points"
    ADD CONSTRAINT season_id FOREIGN KEY ("Season_ID")
    REFERENCES public."Seasons" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."Sessions"
    ADD CONSTRAINT season_id FOREIGN KEY ("Season_ID")
    REFERENCES public."Seasons" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;