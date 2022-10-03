CREATE TABLE public."Clans"
(
    "ID" integer NOT NULL,
    "Name" text NOT NULL,
    PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Clans"
    OWNER to bombotvanderwoodstream;


CREATE TABLE public."Players"
(
    "ID" integer NOT NULL,
    "Name" text NOT NULL,
    "Clan_ID" integer NOT NULL,
    PRIMARY KEY ("ID"),
    CONSTRAINT clan_id FOREIGN KEY ("Clan_ID")
    REFERENCES public."Clans" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID
);

ALTER TABLE IF EXISTS public."Players"
    OWNER to bombotvanderwoodstream;


CREATE TABLE public."Seasons"
(
    "ID" integer NOT NULL,
    "Start_Date" date NOT NULL,
    "End_Date" date,
    PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Seasons"
    OWNER to bombotvanderwoodstream;


CREATE TABLE public."Sessions" (
    "ID" integer NOT NULL,
    "Start_Time" date NOT NULL,
    "End_Time" date,
    "Season_ID" integer NOT NULL,
    PRIMARY KEY ("ID"),
    CONSTRAINT season_id FOREIGN KEY ("Season_ID")
        REFERENCES public."Seasons" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Sessions"
    OWNER to bombotvanderwoodstream;


CREATE TABLE public."Checkins"
(
    "ID" integer NOT NULL,
    "Session_ID" integer NOT NULL,
    "Player_ID" integer NOT NULL,
    PRIMARY KEY ("ID"),
    CONSTRAINT session_id FOREIGN KEY ("Session_ID")
        REFERENCES public."Sessions" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT player_id FOREIGN KEY ("Player_ID")
        REFERENCES public."Players" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Checkins"
    OWNER to bombotvanderwoodstream;


CREATE TABLE public."Points"
(
    "ID" integer NOT NULL,
    "Player_ID" integer NOT NULL,
    "Season_ID" integer NOT NULL,
    "Points" integer NOT NULL DEFAULT 0,
    "Clan_ID" integer NOT NULL,
    PRIMARY KEY ("ID"),
    CONSTRAINT player_id FOREIGN KEY ("Player_ID")
        REFERENCES public."Players" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT season_id FOREIGN KEY ("Season_ID")
        REFERENCES public."Seasons" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT clan_id FOREIGN KEY ("Clan_ID")
        REFERENCES public."Clans" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Points"
    OWNER to bombotvanderwoodstream;