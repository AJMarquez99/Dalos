# DALOS Stock Monitoring

## Overview

## Context

## Goals

The main goal is to incorporate as many modern technologies as possible seamlessly into this small project in order to create a functional web application that may be shown and explained to others. For the project to be a success it must be able to:
- Create and store users.
- Display information and data based on user preferences and decisions.
- Pull and visualize stock data in a format that would allow users to interpret the information with accuracy.


## Milestones

## User Story

A user would go about using Dalos by hopping onto the site and creating an account. Once an account is created then the user may begin searching for stock data, which will conveniently be served using nicely stylized graphs. There will be consistency in the initial information being served. Once a stock has peaked the user’s interest it may be saved into one of multiple user-defined buckets so that they may be cross-compared and analyzed further. 

## Technical Architecture

Dalos will be structured using the Django framework as a basis for serving the front-end pages as well as for managing the functionality of much of the site. Django is the technology of choice here due to its basis in Python, a necessary component of much of the data processing that will be occurring, allowing for seamless connectivity between the front-end and back-end aspects of the project. It will work in partnership with Bootstrap as the CSS framework with a SASS pre-compiler for any custom design changes that will be necessary. The functionality will be built out using Python3 as the language of choice with each major functionality being scoped as its on application within Django. Much of the data being used will be pulled from 3rd-party APIs but the intrinsic data necessary for the site will be stored in a MySQL relational database on RDBMS in AWS. The application itself will be hosted on an EC2 instance for the time being with future plans for horizontal scaling using multiple instances and a load-balancer in order to handle increased traffic. Any static images necessary for the site will be stored in S3 also within AWS and will be utilized by Dalos using a CDN.

## Scoping/Timeline