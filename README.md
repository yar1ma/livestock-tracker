# Livestock GPS Tracker

A GPS-based livestock monitoring system built for cattle, starting with a working prototype rather than a proposal.

## What it does

- Receives and stores an animal's GPS location
- Detects when an animal leaves a defined grazing boundary (geofencing)
- Logs boundary-crossing alerts with a timestamp
- Supports multiple animals at once

## Stack

- Backend: FastAPI, Python
- Database: SQLite
- Simulator: Python script generating fake GPS readings while real hardware is sourced

## Status

Currently running on simulated GPS data. Real GPS hardware is being sourced and will replace the simulator once wired up.

## Related repo

Dashboard: [link to your livestock-dashboard repo]