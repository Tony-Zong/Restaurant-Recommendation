.mode column
.header ON

CREATE TABLE rest_info
  (id integer,
   rest_name varchar(50),
   phone varchar(20),
   street varchar(100),
   city varchar(10),
   zipcode integer,
   website varchar(500),
   num_review integer,
   bayes float,
   vio_occ boolean,
   time_start integer,
   time_end integer,
   risk_val integer,
   rating float,
   price integer,
   constraint rest_info primary key (id));

.separator ","
.import rest_info.csv rest_info


CREATE TABLE words_table
  (id integer,
   word varchar(20),
   constraint fk_words_table foreign key (id)
    references rest_info (id));

.mode column
.header ON
.separator ","
.import words_table.csv words_table