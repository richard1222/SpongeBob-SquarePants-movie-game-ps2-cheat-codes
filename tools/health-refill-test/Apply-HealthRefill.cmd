@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Apply-HealthRefill.ps1" %*
