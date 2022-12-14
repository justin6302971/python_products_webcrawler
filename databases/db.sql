CREATE SCHEMA product_info
    AUTHORIZATION tempuser_local;



CREATE TABLE product_info.product
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 ),
    code text NOT NULL,
    description text,
    status boolean NOT NULL DEFAULT True,
    created_dt timestamp without time zone NOT NULL,
    modified_dt timestamp without time zone,
    is_new_item boolean NOT NULL DEFAULT True,
    notify_counts integer NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS product_info.product
    OWNER to tempuser_local;


-- todo: create unique constraint for product code 