# Mongo Change Stream example

This repo is a toy example for Mongo change streams functionality. It is based on [https://www.mongodb.com/blog/post/an-introduction-to-change-streams](this) example but with some simplifications and changes.

## How to run

On one window: `docker-compose up mongo infinite-write`

On another: `docker-compose up change-stream`

## What does it do

Container `infinite-write` is writing to the Mongo replicaSet a new fruit/quantity pair each second.

Meanwhile the `change-stream` container is watching Mongo changes to find `insert` operations where the fruit starts with letter `p`.
