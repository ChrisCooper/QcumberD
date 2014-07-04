FROM postgres:14.04

MAINTAINER Chris Cooper <chriscooper1991@gmail.com>

# Docker hosting - #http://www.tutum.co/pricing/

# Update packages
RUN apt-get update -qq

RUN apt-get install -y python-psycopg2