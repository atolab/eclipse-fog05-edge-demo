#!/usr/bin/env bash

sudo systemctl start yaks
sudo systemctl start fosagent
sudo systemctl start foslinux
sudo systemctl start foslinuxbridge
sudo systemctl start foslxd
sudo systemctl start fosctd
sudo systemctl start fosnative


sudo systemctl status yaks
sudo systemctl status fosagent
sudo systemctl status foslinux
sudo systemctl status foslinuxbridge
sudo systemctl status foslxd
sudo systemctl status fosctd
sudo systemctl status fosnative