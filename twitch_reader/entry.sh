#!/bin/bash
python /twitch_reader/base_generator.py
mv /twitch_reader/example_website/* /wwwroot/
crond -f
