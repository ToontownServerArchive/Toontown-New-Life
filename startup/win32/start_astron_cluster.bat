@echo off
title Astron
cd ../../astron
astrond --loglevel debug config/cluster_yaml.yml
pause