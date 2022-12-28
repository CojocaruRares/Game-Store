CREATE TABLE category (
    category_id NUMBER(3) NOT NULL,
    genre       VARCHAR2(200) NOT NULL,
    platform    VARCHAR2(100) NOT NULL
)
LOGGING;

ALTER TABLE category ADD CHECK ( length(genre) > 1 ) ;

ALTER TABLE category ADD CONSTRAINT category_pk PRIMARY KEY ( category_id );

CREATE TABLE clients (
    client_id  NUMBER(3) NOT NULL,
    first_name VARCHAR2(100) NOT NULL,
    last_name  VARCHAR2(100),
    wallet     NUMBER(12, 2) NOT NULL
)
LOGGING;

ALTER TABLE clients ADD CHECK ( length(first_name) > 2 );

ALTER TABLE clients ADD CHECK ( wallet >= 0 ) ;

ALTER TABLE clients ADD CONSTRAINT clients_pk PRIMARY KEY ( client_id );

CREATE TABLE contactinfo (
    clients_client_id NUMBER(3) NOT NULL,
    email             VARCHAR2(50) NOT NULL,
    phone             VARCHAR2(11)
)
LOGGING;

ALTER TABLE contactinfo ADD CHECK ( REGEXP_LIKE ( email,
                                                  '[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}' ) );

ALTER TABLE contactinfo ADD CHECK (REGEXP_LIKE ( phone,
                                                  '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' ) );

ALTER TABLE contactinfo ADD CONSTRAINT contactinfo_pk PRIMARY KEY ( clients_client_id );

CREATE TABLE developer (
    developer_id   NUMBER(3) NOT NULL,
    developer_name VARCHAR2(200)
)
LOGGING;

ALTER TABLE developer ADD CHECK ( length(developer_name) > 1 );

ALTER TABLE developer ADD CONSTRAINT developer_pk PRIMARY KEY ( developer_id );

CREATE TABLE transactions (
    transaction_id        NUMBER(3) NOT NULL,
    transaction_date      DATE,
    videogames_product_id NUMBER(3) NOT NULL,
    clients_client_id     NUMBER(3) NOT NULL
)
LOGGING;

ALTER TABLE transactions ADD CONSTRAINT transactions_pk PRIMARY KEY ( transaction_id );

CREATE TABLE videogames (
    product_id             NUMBER(3) NOT NULL,
    product_name           VARCHAR2(200),
    price                  NUMBER(6, 2) NOT NULL,
    developer_developer_id NUMBER(3) NOT NULL,
    category_category_id   NUMBER(3) NOT NULL
)
LOGGING;

ALTER TABLE videogames ADD CHECK ( length(product_name) > 1 ) ;

ALTER TABLE videogames ADD CHECK ( price >= 0 ) ;

ALTER TABLE videogames ADD CONSTRAINT videogames_pk PRIMARY KEY ( product_id );

ALTER TABLE contactinfo
    ADD CONSTRAINT contactinfo_clients_fk FOREIGN KEY ( clients_client_id )
        REFERENCES clients ( client_id )
    NOT DEFERRABLE;

ALTER TABLE transactions
    ADD CONSTRAINT transactions_clients_fk FOREIGN KEY ( clients_client_id )
        REFERENCES clients ( client_id )
    NOT DEFERRABLE;

ALTER TABLE transactions
    ADD CONSTRAINT transactions_videogames_fk FOREIGN KEY ( videogames_product_id )
        REFERENCES videogames ( product_id )
    NOT DEFERRABLE;

ALTER TABLE videogames
    ADD CONSTRAINT videogames_category_fk FOREIGN KEY ( category_category_id )
        REFERENCES category ( category_id )
    NOT DEFERRABLE;

ALTER TABLE videogames
    ADD CONSTRAINT videogames_developer_fk FOREIGN KEY ( developer_developer_id )
        REFERENCES developer ( developer_id )
    NOT DEFERRABLE;

CREATE OR REPLACE TRIGGER Trg_Transactions_BRIU 
    BEFORE INSERT OR UPDATE ON TRANSACTIONS
    FOR EACH ROW 
BEGIN
IF( :new.transaction_date <= SYSDATE-1 )
THEN
RAISE_APPLICATION_ERROR( -20001,
'Data invalida: ' || TO_CHAR( :new.transaction_date, 'DD.MM.YYYY HH24:MI:SS' ) || ' trebuie sa fie mai mare decat data curenta.' );
END IF;
END; 
/

CREATE SEQUENCE category_category_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER category_category_id_trg BEFORE
    INSERT ON category
    FOR EACH ROW
    WHEN ( new.category_id IS NULL )
BEGIN
    :new.category_id := category_category_id_seq.nextval;
END;
/

CREATE SEQUENCE clients_client_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER clients_client_id_trg BEFORE
    INSERT ON clients
    FOR EACH ROW
    WHEN ( new.client_id IS NULL )
BEGIN
    :new.client_id := clients_client_id_seq.nextval;
END;
/

CREATE SEQUENCE developer_developer_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER developer_developer_id_trg BEFORE
    INSERT ON developer
    FOR EACH ROW
    WHEN ( new.developer_id IS NULL )
BEGIN
    :new.developer_id := developer_developer_id_seq.nextval;
END;
/

CREATE SEQUENCE transactions_transaction_id START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER transactions_transaction_id BEFORE
    INSERT ON transactions
    FOR EACH ROW
    WHEN ( new.transaction_id IS NULL )
BEGIN
    :new.transaction_id := transactions_transaction_id.nextval;
END;
/

CREATE SEQUENCE videogames_product_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER videogames_product_id_trg BEFORE
    INSERT ON videogames
    FOR EACH ROW
    WHEN ( new.product_id IS NULL )
BEGIN
    :new.product_id := videogames_product_id_seq.nextval;
END;
/