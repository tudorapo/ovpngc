# A simple script to get OpenVPN config

OpenVPN has a nice paying feature called [Access
Server](https://openvpn.net/vpn-server/). My company uses it and macs were able
to get the configuration, but me with my linux laptop was left stranded.

Until I found out that the Access Server has a [nice
API](https://openvpn.net/images/pdf/REST_API.pdf) to solve this problem. It can
be done manually by curl, but it's easier this way. 

Also I don't have much access yet so I had time.

## TODO:

- Was not able to test the GetAutoLogin thing

- The configuration asks for the DNS server(s) but does not contains directions
  about what to do with them. Add these lines to the resulting configuration:
```
script-security 2
# up /etc/openvpn/update-resolv-conf
# down /etc/openvpn/update-resolv-conf
up /etc/openvpn/scripts/update-systemd-resolved
down /etc/openvpn/scripts/update-systemd-resolved
```
  The systemd scripts can be downloaded from
  [here](https://raw.githubusercontent.com/jonathanio/update-systemd-resolved/master/update-systemd-resolved).


