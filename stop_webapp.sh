#!/bin/bash

# Kill Flask Python server
kill $(lsof -t -i:5000)

# Kill React frontend
kill $(lsof -t -i:3000)
