# Translation of Slang Posts

Python script to translate slang posts.

## Introduction

This script search and replace slang words based in the postgres database.

### Database Structure

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA public;

ALTER SCHEMA public OWNER TO postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

CREATE FUNCTION public.sem_acentos(character varying) RETURNS character varying
    LANGUAGE sql
    AS $_$
SELECT TRANSLATE($1, 'áéíóúàèìòùãõâêîôôäëïöüçÁÉÍÓÚÀÈÌÒÙÃÕÂÊÎÔÛÄËÏÖÜÇ', 'aeiouaeiouaoaeiooaeioucAEIOUAEIOUAOAEIOOAEIOUC')
$_$;

ALTER FUNCTION public.sem_acentos(character varying) OWNER TO sbsadmin;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE public.classe (
    idclasse integer NOT NULL,
    nome character varying(80) NOT NULL
);


ALTER TABLE public.classe OWNER TO sbsadmin;

CREATE TABLE public.classificacaocubo (
    idclassificacao integer NOT NULL,
    nome character varying(80) NOT NULL,
    nomeoriginal character varying(80) NOT NULL
);


ALTER TABLE public.classificacaocubo OWNER TO sbsadmin;

CREATE TABLE public.expressaocategorizada (
    idexpressao integer NOT NULL,
    descricao character varying(120) NOT NULL,
    idsubclasse character varying(20) NOT NULL,
    idclasse integer,
    dssignificado character varying(350),
    dssignificadooriginal character varying(350),
    quantpalavras integer
);


ALTER TABLE public.expressaocategorizada OWNER TO sbsadmin;

CREATE TABLE public.ontcexp (
    id_str text,
    text text,
    created_at text,
    idseq integer NOT NULL
);


ALTER TABLE public.ontcexp OWNER TO sbsadmin;

CREATE SEQUENCE public.seq_postagem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_postagem OWNER TO sbsadmin;

CREATE TABLE public.postagem (
    idpostagem integer DEFAULT nextval('public.seq_postagem'::regclass) NOT NULL,
    identificarmensagem character varying(120) NOT NULL,
    mensagem text NOT NULL,
    mensagemoriginal text,
    postcandidata character varying(20),
    idclassificacao integer
);


ALTER TABLE public.postagem OWNER TO sbsadmin;

CREATE TABLE public.postagemtermo (
    idpostagem integer NOT NULL,
    idtermo integer NOT NULL
);


ALTER TABLE public.postagemtermo OWNER TO sbsadmin;

CREATE SEQUENCE public.seq_ontcexp
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seq_ontcexp OWNER TO sbsadmin;


CREATE TABLE public.significado (
    idsignificado integer NOT NULL,
    descricao character varying(120) NOT NULL
);


ALTER TABLE public.significado OWNER TO sbsadmin;

CREATE TABLE public.subclasse (
    idsubclasse character varying(15) NOT NULL,
    descricao character varying(120) NOT NULL,
    idclasse integer
);


ALTER TABLE public.subclasse OWNER TO sbsadmin;

CREATE TABLE public.termo (
    idtermo integer NOT NULL,
    descricao character varying(120) NOT NULL,
    idclasse integer,
    nivelrelevancia integer,
    descadaptada character varying(120),
    significadooriginal character varying(800),
    qtdepalavras integer
);


ALTER TABLE public.termo OWNER TO sbsadmin;

CREATE TABLE public.termosignificado (
    idtermo integer NOT NULL,
    idsignificado integer NOT NULL
);


ALTER TABLE public.termosignificado OWNER TO sbsadmin;

CREATE TABLE public.termoversionamento (
    idtermo integer NOT NULL,
    dataversao date NOT NULL,
    descricao character varying(120) NOT NULL,
    idclasse integer,
    nivelrelevancia integer,
    descadaptada character varying(120),
    significadooriginal character varying(800)
);


ALTER TABLE public.termoversionamento OWNER TO sbsadmin;


ALTER TABLE ONLY public.classe
    ADD CONSTRAINT classe_pkey PRIMARY KEY (idclasse);

ALTER TABLE ONLY public.classificacaocubo
    ADD CONSTRAINT classificacao_pkey PRIMARY KEY (idclassificacao);

ALTER TABLE ONLY public.expressaocategorizada
    ADD CONSTRAINT expressaocategorizada_pkey PRIMARY KEY (idexpressao);

ALTER TABLE ONLY public.ontcexp
    ADD CONSTRAINT ontcexp_pkey PRIMARY KEY (idseq);

ALTER TABLE ONLY public.postagem
    ADD CONSTRAINT postagem_pkey PRIMARY KEY (idpostagem);

ALTER TABLE ONLY public.postagemtermo
    ADD CONSTRAINT postagemtermo_pkey PRIMARY KEY (idpostagem, idtermo);

ALTER TABLE ONLY public.significado
    ADD CONSTRAINT significado_pkey PRIMARY KEY (idsignificado);

ALTER TABLE ONLY public.subclasse
    ADD CONSTRAINT subclasse_pkey PRIMARY KEY (idsubclasse);

ALTER TABLE ONLY public.termo
    ADD CONSTRAINT termo_pkey PRIMARY KEY (idtermo);

ALTER TABLE ONLY public.termosignificado
    ADD CONSTRAINT termosignificado_pkey PRIMARY KEY (idtermo, idsignificado);


ALTER TABLE ONLY public.termoversionamento
    ADD CONSTRAINT termoversio_pkey PRIMARY KEY (idtermo, dataversao);

CREATE INDEX postagem_mensagem_idx ON public.postagem USING btree (mensagem);

ALTER TABLE ONLY public.expressaocategorizada
    ADD CONSTRAINT fk_expressaocategorizada_classe FOREIGN KEY (idclasse) REFERENCES public.classe(idclasse);

ALTER TABLE ONLY public.postagemtermo
    ADD CONSTRAINT fk_postagem_has_termo_postagem1 FOREIGN KEY (idpostagem) REFERENCES public.postagem(idpostagem);

ALTER TABLE ONLY public.postagemtermo
    ADD CONSTRAINT fk_postagem_has_termo_termo1 FOREIGN KEY (idtermo) REFERENCES public.termo(idtermo);

ALTER TABLE ONLY public.subclasse
    ADD CONSTRAINT fk_subclasse_classe FOREIGN KEY (idclasse) REFERENCES public.classe(idclasse);

ALTER TABLE ONLY public.termo
    ADD CONSTRAINT fk_termo_classe FOREIGN KEY (idclasse) REFERENCES public.classe(idclasse);

ALTER TABLE ONLY public.termosignificado
    ADD CONSTRAINT fk_termo_has_significado_significado1 FOREIGN KEY (idsignificado) REFERENCES public.significado(idsignificado);

ALTER TABLE ONLY public.termosignificado
    ADD CONSTRAINT fk_termo_has_significado_termo1 FOREIGN KEY (idtermo) REFERENCES public.termo(idtermo);

ALTER TABLE ONLY public.termoversionamento
    ADD CONSTRAINT fk_termoversio_classe FOREIGN KEY (idclasse) REFERENCES public.classe(idclasse);

ALTER TABLE ONLY public.postagem
    ADD CONSTRAINT "pfClassificacaoCube" FOREIGN KEY (idclassificacao) REFERENCES public.classificacaocubo(idclassificacao) ON UPDATE RESTRICT ON DELETE RESTRICT;

