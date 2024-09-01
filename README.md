# nogfi-hackathon v1

Thie repository contains example tasks and code samples for nog.fi hackathon. 


## Project structure

This project is built based on [rye](https://rye.astral.sh) but you can install the same modules/dependencies by using other tools, like pip.

Rye can be installed for linux/mac with following command

```bash
curl -sSf https://rye.astral.sh/get | bash
```

The further installation instructions, including Windows binaries, can be found here, https://rye.astral.sh/guide/installation/.

```bash
# rye --version
rye 0.39.0
commit: 0.39.0 (bf3ccf818 2024-08-21)
platform: linux (x86_64)
self-python: cpython@3.12.4
symlink support: true
uv enabled: true
```


Once you have installed rye, clone the project and run

```bash
rye sync
```

this will install all the needed dependencies to run the tasks.

If you prefer to manage the python env and dependencies via some other way, for example via pip

```bash
pip install -r requirements.txt
```


## Lab devices

The lab devices consist of virtual lab devices and simulated devices with [fakenos](https://github.com/fakenos/fakenos).

The virtual lab devices should be primary way to test your code as those have the full control/data/mgmt plane and it allows you to run any kind of tests. However, there are limited number of  different NOSes and devices available for testing the scalability of your code.

FakeNOS is a simulator, it does not emulate any of Network Control, Data or Management planes, it merely takes the commands as input and responds with predefined output. However, it's possible to simulate access to 100s of devices.

### Lab device access

\<add description here\>

### Fakenos devices

Fakenos simulation can be run on your own laptop. You can start the simulated devices based on the yaml configuration file, in which you define the desired platform, user/pass and the port. The available platforms can be found [here](https://fakenos.github.io/fakenos/platforms/)

```yml
hosts:
  R1:
    username: admin
    password: admin
    platform: cisco_ios
    port: 6000
  R2:
    username: admin
    password: admin
    platform: hp_comware
    port: 6001
  R3:
    username: admin
    password: admin
    platform: dell_force10
    port: 6002
```

Running the command, will spin up 3 instances

```bash
# rye run fakenos --inventory src/nogfi_hackathon/fakenos/inventory_small.yaml 
Initiating FakeNOS
INFO:fakenos.plugins.utils.cli:Initiating FakeNOS
INFO:fakenos.core.fakenos:The following devices has been initiated: ['R1', 'R2', 'R3']
INFO:fakenos.core.fakenos:Device R1 is running on port 6000
INFO:fakenos.core.fakenos:Device R2 is running on port 6001
INFO:fakenos.core.fakenos:Device R3 is running on port 6002
```

and after that you can login to the devices

```bash
# ssh admin@localhost -p 6000
FakeNOS Paramiko SSH Server
admin@localhost's password: 
Custom SSH Shell
R1>show version
Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.8(3)M2, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2019 by Cisco Systems, Inc.
Compiled Thu 28-Mar-19 14:06 by prod_rel_team


ROM: Bootstrap program is IOSv

rtr-01 uptime is 1 week, 3 days, 16 hours, 11 minutes
System returned to ROM by reload
System image file is "flash0:/vios-adventerprisek9-m"
Last reload reason: Unknown reason
 


This product contains cryptographic features and is subject to United
 States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.
 
A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.
 
Cisco IOSv (revision 1.0) with  with 460137K/62464K bytes of memory.
Processor board ID 991UCMIHG4UAJ1J010CQG
4 Gigabit Ethernet interfaces
DRAM configuration is 72 bits wide with parity disabled.
256K bytes of non-volatile configuration memory.
2097152K bytes of ATA System CompactFlash 0 (Read/Write)
0K bytes of ATA CompactFlash 1 (Read/Write)
11217K bytes of ATA CompactFlash 2 (Read/Write)
 0K bytes of ATA CompactFlash 3 (Read/Write)



Configuration register is 0x0
```


It's also possible to spin up larger range of devices

```yml
hosts:
  ios:
    username: admin
    password: admin
    platform: cisco_ios
    port: 
      - 6001
      - 6100
    replicas: 100
```

```bash
# rye run fakenos --inventory src/nogfi_hackathon/fakenos/inventory_100_ios.yaml 
Initiating FakeNOS
INFO:fakenos.plugins.utils.cli:Initiating FakeNOS
INFO:fakenos.core.fakenos:The following devices has been initiated: ['ios56', 'ios28', 'ios61', 'ios11', 'ios41', 'ios49', 'ios79', 'ios92', 'ios52', 'ios53', 'ios14', 'ios60', 'ios86', 'ios97', 'ios88', 'ios48', 'ios35', 'ios25', 'ios24', 'ios18', 'ios51', 'ios50', 'ios69', 'ios2', 'ios8', 'ios89', 'ios96', 'ios94', 'ios82', 'ios59', 'ios37', 'ios40', 'ios72', 'ios10', 'ios66', 'ios80', 'ios38', 'ios68', 'ios17', 'ios43', 'ios75', 'ios62', 'ios42', 'ios27', 'ios76', 'ios54', 'ios21', 'ios64', 'ios81', 'ios39', 'ios6', 'ios22', 'ios57', 'ios46', 'ios34', 'ios36', 'ios83', 'ios93', 'ios99', 'ios1', 'ios29', 'ios5', 'ios4', 'ios3', 'ios90', 'ios58', 'ios16', 'ios7', 'ios0', 'ios13', 'ios31', 'ios9', 'ios15', 'ios84', 'ios73', 'ios65', 'ios44', 'ios45', 'ios47', 'ios71', 'ios85', 'ios78', 'ios74', 'ios67', 'ios98', 'ios87', 'ios63', 'ios77', 'ios26', 'ios55', 'ios33', 'ios30', 'ios32', 'ios20', 'ios19', 'ios23', 'ios91', 'ios12', 'ios70', 'ios95']
INFO:fakenos.core.fakenos:Device ios56 is running on port 6001
INFO:fakenos.core.fakenos:Device ios28 is running on port 6002
INFO:fakenos.core.fakenos:Device ios61 is running on port 6003
INFO:fakenos.core.fakenos:Device ios11 is running on port 6004
INFO:fakenos.core.fakenos:Device ios41 is running on port 6005
INFO:fakenos.core.fakenos:Device ios49 is running on port 6006
```