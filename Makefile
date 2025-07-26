# simple makefile for thalatlas
# 'make all' will run both placeholder scripts

all:
   python scripts/test_lookup.py
   python scripts/visualize_seas.py

