# Contento

This is a tool to post content to social media platforms, like Twitter, Instagram, etc.
Posts can be planed ahead and scheduled to be posted at a specific date and time.

## Motivation

Tools like this already exist, but are ridiculously expensive for the little service they provide.
This repo provides a way to build, use and host such a tool yourself.

## Code stack

Posts are stored inside json files.
There exists a streamlit application to manage those json files. It can be started using streamlit run json_file_manager.
In order for the json files to be posted to their respective platforms the main.py function is used. It checks each jsons inside all "post_queue" folders and compares its intended post datetime with the current datetime. If the intended post datetime lies in the past, the content from the json files gets posted immediately.
In order to achieve automated posting, a cron job should be implemented that runs the main function for example every 10 minutes.
