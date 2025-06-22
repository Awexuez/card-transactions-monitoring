

DROP TABLE IF EXISTS card_transactions;

CREATE TABLE card_transactions(
	transaction_id bigserial NOT NULL,
	amount numeric(15,2) NOT NULL,
	transaction_date timestamp NOT NULL,
	delete_flag boolean DEFAULT FALSE,
	CONSTRAINT card_transacttions_pkey PRIMARY KEY (transaction_id)
);


SELECT * FROM card_transactions;
