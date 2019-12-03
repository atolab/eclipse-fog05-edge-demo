#!/usr/bin/env bash

sudo systemctl stop fosnative
sudo systemctl stop foslxd
sudo systemctl stop fosctd
sudo systemctl stop foslinuxbridge
sudo systemctl stop foslinux
sudo systemctl stop fosagent
sudo systemctl stop yaks



sudo systemctl status yaks
sudo systemctl status fosagent
sudo systemctl status foslinux
sudo systemctl status foslinuxbridge
sudo systemctl status foslxd
sudo systemctl status fosctd
sudo systemctl status fosnative