-- Databricks notebook source
drop schema if exists clinical.bronze cascade;
drop schema if exists clinical.silver cascade;
drop schema if exists clinical.gold cascade;

-- COMMAND ----------

create schema if not exists clinical.bronze;
create schema if not exists clinical.silver;
create schema if not exists clinical.gold;
