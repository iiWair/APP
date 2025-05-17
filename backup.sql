--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cart_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cart_item (
    id integer NOT NULL,
    user_id integer NOT NULL,
    offer_id integer NOT NULL
);


--
-- Name: cart_item_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cart_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cart_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cart_item_id_seq OWNED BY public.cart_item.id;


--
-- Name: offer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.offer (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(500),
    price double precision NOT NULL,
    available boolean
);


--
-- Name: offer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.offer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: offer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.offer_id_seq OWNED BY public.offer.id;


--
-- Name: ticket; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ticket (
    id integer NOT NULL,
    purchase_key character varying(100) NOT NULL,
    qr_code_path character varying(120) NOT NULL,
    created_at timestamp without time zone,
    user_id integer NOT NULL,
    offer_id integer NOT NULL,
    "timestamp" timestamp without time zone
);


--
-- Name: ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ticket_id_seq OWNED BY public.ticket.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    email character varying(150) NOT NULL,
    password character varying(200) NOT NULL,
    secret_key character varying(255) NOT NULL,
    is_admin boolean
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: cart_item id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item ALTER COLUMN id SET DEFAULT nextval('public.cart_item_id_seq'::regclass);


--
-- Name: offer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer ALTER COLUMN id SET DEFAULT nextval('public.offer_id_seq'::regclass);


--
-- Name: ticket id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket ALTER COLUMN id SET DEFAULT nextval('public.ticket_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: cart_item; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cart_item (id, user_id, offer_id) FROM stdin;
\.


--
-- Data for Name: offer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.offer (id, name, description, price, available) FROM stdin;
1	Basketball	Venez assister au match d'ouverture de basketball	150	t
2	100 m	Lors de cette course  vous découvrirez quelle pays l'emportera	125	t
3	Gymnastique Artistique	Venez découvrir qui remportera la médaille 	175	t
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ticket (id, purchase_key, qr_code_path, created_at, user_id, offer_id, "timestamp") FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (id, username, email, password, secret_key, is_admin) FROM stdin;
1	test	test@gmail.com	scrypt:32768:8:1$2TT5zzeCtAuxaMVX$83eff1eded15d2f5a0dff7d468e3b13c39fb62b58979d0eaf57901d1de7e375a965e4d6e2e436d7a866c01ae6f9e08e2d93fdd9028b228ad5c788ffe7ca8e43e	8761c4fe8b3e3f4e79bc85e2ad7b42a7ecf700a4c928046c149675cc924e18cd	f
4	thom	thomasboundaoui91180@gmail.com	$2b$12$X4OJj2YKVUBlwVl7PgsL3ewf2/MNYTQUiwZKgJox10b5RtwY.WyJ2	3744ccd28929b529e12c6995e2205ef8044eb4fc5d32721d50b47254f6da2c2f	f
2	admin	admin@example.com	$2b$12$znd9ErcnKF0SmiXBNdxiL.ZsNBXFuPwmCixFT7B3.4j3VwFiwBbZ2	b29c1a2d8a604e6fa83910a9f0bfc7359e0a3ed23ec96b0e6a45f1b1a5cf58dc	t
\.


--
-- Name: cart_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cart_item_id_seq', 1, false);


--
-- Name: offer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.offer_id_seq', 3, true);


--
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ticket_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_id_seq', 4, true);


--
-- Name: cart_item cart_item_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_pkey PRIMARY KEY (id);


--
-- Name: offer offer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.offer
    ADD CONSTRAINT offer_pkey PRIMARY KEY (id);


--
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);


--
-- Name: ticket ticket_purchase_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_purchase_key_key UNIQUE (purchase_key);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: cart_item cart_item_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offer(id);


--
-- Name: cart_item cart_item_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: ticket ticket_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_offer_id_fkey FOREIGN KEY (offer_id) REFERENCES public.offer(id);


--
-- Name: ticket ticket_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

