### Overview

These instructions walk you through setting up an AD server on a CentOS 7 host for use with BlueData and then configuring BlueData to use the AD server.

### Script to create some AD users and groups

First create a file (e.g. `/home/centos/ad_user_setup.sh`) with these contents: 


```bash
#!/bin/bash
	 
# allow weak passwords - easier to demo
samba-tool domain passwordsettings set --complexity=off
	    
# Create DemoTenantUsers group and a user ad_user1
samba-tool group add DemoTenantUsers
samba-tool user create ad_user1 pass123
samba-tool group addmembers DemoTenantUsers ad_user1

# Create DemoTenantAdmins group and a user ad_admin1
samba-tool group add DemoTenantAdmins
samba-tool user create ad_admin1 pass123
samba-tool group addmembers DemoTenantAdmins ad_admin1
```

Read the comments to understand what the file does.

### Setup docker on the AD Host

Setup docker and openldap client:

```bash
sudo yum install -y docker openldap-clients
sudo service docker start
sudo systemctl enable docker
```

# Run Samba AD server docker image

Run the image (note the `ad_user_setup.sh` script path is passed as a parameter):

```bash
sudo docker run --privileged --restart=unless-stopped \
       -p 53:53 -p 53:53/udp -p 88:88 -p 88:88/udp -p 135:135 -p 137-138:137-138/udp -p 139:139 -p 389:389 \
       -p 389:389/udp -p 445:445 -p 464:464 -p 464:464/udp -p 636:636 -p 1024-1044:1024-1044 -p 3268-3269:3268-3269 \
       -e "SAMBA_DOMAIN=samdom" \
       -e "SAMBA_REALM=samdom.example.com" \
       -e "SAMBA_ADMIN_PASSWORD=5ambaPwd@" \
       -e "ROOT_PASSWORD=R00tPwd@" \
       -e "LDAP_ALLOW_INSECURE=true" \
       -e "SAMBA_HOST_IP=$(hostname --all-ip-addresses |cut -f 1 -d' ')" \
       -v /home/centos/ad_user_setup.sh:/usr/local/bin/custom.sh \
       --name samdom \
       --dns 127.0.0.1 \
       -d \
       --entrypoint "/bin/bash" \
       rsippl/samba-ad-dc \
       -c "chmod +x /usr/local/bin/custom.sh &&. /init.sh app:start
```

### BlueData UI Configuration

You can configure BlueData Settings in the BlueData UI:

```
System Settings -> User Authentication
   -> Authentication Type: Active Directory
   -> Security Protocol: LDAPS
   -> Service Location: <<your_ad_server_ip>> | Port: 636
   -> Bind Type: Search Bind
   -> User Attribute: sAMAccountName
   -> Base DN: CN=Users,DC=samdom,DC=example,DC=com
   -> Bind DN: cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com
   -> Bind Password: 5ambaPwd@
```

Configure a tenant (e.g. Demo Tenant) in the BlueData UI with:

```
Tenant Settings
  -> External User Groups: CN=DemoTenantAdmins,CN=Users,DC=samdom,DC=example,DC=com | Admin
  -> External User Groups: CN=DemoTenantUsers,CN=Users,DC=samdom,DC=example,DC=com | Member
```

The `DemoTenantAdmins` and `DemoTenantUsers` groups are created by the `ad_user_setup.sh` script.

You can then login to the BlueData UI tenant with these users (these users are created by the `ad_user_setup.sh` script:

 - Member: `ad_user1/pass123` 
 - Admin: `ad_admin1/pass123`
 
### Using AD

Provision a Spark + JupyterHub cluster.

- Login to Jupyterhub using the AD users
- Login to ssh using the AD users
  - Try running `sudo ls /` as both users.  With the default tenant settings on 4.x  ...
    - ad_user1 will not be able to run sudo as they are in the Member group
    - ad_admin1 will be able to run sudo as they are in the Admin group
  - Try changing [superuser privileges](http://docs.bluedata.com/40_editing-an-existing-tenant-or-project) and try running `sudo ls /` again 


### AD Tree browser

You can connect to your AD instance with Apache Directory Studio (useful for understanding the AD objects that have been created):

```
In Apache Directory Studio, create a new connection:
   -> Connection name: choose something meaningful
   -> Hostname: <<your_ad_server_ip>>
   -> Port: 636
   -> Connection timeout(s): 30
   -> Encryption method: No encryption
   -> Provider: Apache Directory LDAP Client API
Click Next
   -> Authentication Method: Simple Authentication
   -> Bind DN or user: cn=Administrator,CN=Users,DC=samdom,DC=example,DC=com
   -> Bind password: 5ambaPwd@
Click Finish
```
