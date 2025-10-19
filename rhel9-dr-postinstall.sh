clear

# genpop or dbserver template validation 

genpopserver=10.190.4.6
dbserver=10.190.4.7

if [[ $(nmcli con show ens192 | grep ipv4.addresses | grep $dbserver/23 | wc -l) -eq 1 ]]; then
echo
echo "THIS IS FOR THE DR RHEL9 DB BUILDS"
echo
echo "This is the actual result"
nmcli con show ens192 | grep ipv4.addresses | grep $dbserver/23
echo
echo "Before proceeding verify that you are needing a DB server"
echo

elif [[ $(nmcli con show ens192 | grep ipv4.addresses | grep $genpopserver/23 | wc -l) -eq 1 ]]; then

echo
echo "THIS IS FOR THE DR RHEL9 GENPOP BUILDS"
echo
echo "This is the actual result"
nmcli con show ens192 | grep ipv4.addresses | grep $genpopserver/23
echo
echo "Before proceeding verify that you are needing a Genpop server"
echo

else
echo
echo "Program is exiting because as per nmcli con show ens192 | grep ipv4.addresses it is neither $genpopserver
 nor $dbserver"
echo "This is the actual result"
nmcli con show ens192 | grep ipv4.addresses
echo
exit
fi

### end

# This sets the ip and env check variables

envipcheck=10.190
envcheck=dr
### end

# This confirms if it is truely a new server using adinfo

allready1=$(adinfo | grep "Local host name" | grep -v grep | wc -l)

if [[ $allready -ne 0 ]];then
echo "This part of script ran adinfo and either its already started or completed"
echo "see below"
adinfo
echo
exit
fi

### end

# Stating what this program will do and asking to respond with y

echo
echo
echo "This is a clone template. The program will set the network setting;
register the server to the Satelite install Centrify; do a yum update"
echo
echo "Do you wish to continue ? enter y to continue "
read doit

if  [[ "$doit" != y ]];then
echo
echo "y was not entered program has exit or time for response has expired"
exit
fi

### end

# This will ask for ip to which everything will be configured by
# It will validate that it is not less than .10 nor greater or equal to .250

echo
echo
echo "This will update ip and hostname 
The program will exit if less than xx.xx.x.10 or greater or equal to xx.xx.x.250"
echo
echo "Enter the ip of new server"
read ip

ipcheck=$( echo $ip | grep "$envipcheck" | grep -v grep | wc -l)

if [[ $ipcheck -ne 1 ]];then
echo
echo "$ip ip is invalid program will exit.
This is for the $envcheck and $envipcheck network"
echo
exit
fi

iprange=$(echo $ip | cut -d "." -f 4)
if [[ $iprange -lt 10 ]]; 
then 
echo
    echo "$ip is less then xx.xx.x.10
We should not be using ip's less than .10 "
echo
exit
fi

if [[ $iprange -ge 250 ]]; 
then
echo
    echo "$ip is greater then xx.xx.x.250
We should not be using ip's less than .250 "
echo
exit
fi


### end

# This creates ip

echo
ipfile=/etc/NetworkManager/system-connections/ens192.nmconnection
bkdir=/root/post_rhel9_dr_build/Backups/
cp $ipfile ${bkdir}.

echo  "Running nmcli connection modify ens192 ipv4.addresses $ip/23"
nmcli connection modify ens192 ipv4.addresses $ip/23
echo

nmcli connection reload

systemctl restart NetworkManager

### end

# This add hostname from the ip

gethost=$(nslookup $ip | awk '{print $NF}' | sed 's/local./local/' | head -1)

nmcli general hostname $gethost

### end

# This Confirms host and ip

echo
echo
echo "The server will be registered to the Satelite server as follows."
echo
hostname
echo $ip
echo
echo "Respond with y if correct "
read hostit

if  [[ "$hostit" != y ]];then
echo
echo " y was not entered program has exit."
hostname
exit
fi

### end

# Registering to Satelite server

echo
echo Registering $gethost with Satelite server

echo
echo "The true curl command may not be here or has failed due to an expired token
check the following Satellite WebUI --> Hosts --> Register Host --> Advanced --> Find the Token life time checkbox and check it to set it as unlimited."

curl -sS --insecure 'https://lnx-satprd.fnb.cfbi.local/register?activation_keys=DR-RHEL9&force=true&location_id=2&organization_id=1&setup_remote_execution=true&update_packages=false' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJpYXQiOjE3MDU1MjY5NjUsImp0aSI6IjA4Y2U1YTliNzc2MmEzZDE0ZTg1YmUxMThlZDFmNjRiZGE2ODYyZWRjYjJmMGU0NjJmNTMyNjBkZGEyZTk1ZDQiLCJleHAiOjE4ODU1MjY5NjUsInNjb3BlIjoicmVnaXN0cmF0aW9uI2dsb2JhbCByZWdpc3RyYXRpb24jaG9zdCJ9.UyUAsVGbeb2XJEA1I1ItY7feGg0ef2lX8SxvxUXt6Mw' | bash

### end

sleep 2 

# Installing CentrifyDC

echo
echo "Installing CentrifyDC client and excluding CentrifyDC-openssh*"

echo "exclude=CentrifyDC-openssh*" >> /etc/yum.conf
yum install -y CentrifyDC
sed -i s/^'\# adjoin.samaccountname.length\: 15'/'adjoin.samaccountname.length\: 19'/g /etc/centrifydc/centrifydc.conf

### end

# Registering host to Delinea

id=$(cat /root/.secret_for_delinea/.id.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000  -salt -pass pass:Secret@123#)

pass=$(cat /root/.secret_for_delinea/.pass.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000  -salt -pass pass:Secret@123#)

hncount=$(hostname -s | wc -m)
hnlimit=19
hntr=$(hostname -s | head -c $hnlimit)
shorthost=$(hostname -s)
if [[ $hncount -gt $hnlimit ]]; then

echo $shorthost has $hncount characters in its name and is greater the limit of $hnlimit for Delinea
echo In the pre-win2k field in adinfo $shorthost may show up as $hntr

adjoin -n `hostname -s` -c fnb.cfbi.local/Centrify/servers/RedHat-DR -z Global -u $id -p $pass -f fnb.cfbi.local

else
echo

adjoin -n `hostname -s` -N `hostname -s`  -c fnb.cfbi.local/Centrify/servers/RedHat-DR -z Global -u $id -p $pass -f fnb.cfbi.local

fi

if [[ $(adinfo | grep CentrifyDC | grep connected | grep -v grep | wc -l) -eq 0 ]]; then
echo
echo "The automated process seems to have failed adinfo does not show a connection"
adinfo
echo "Run the following

 /root/post_rhel9_dr_build/Run_If_Postinstall_Fails/manual-centrify.sh"

fi

### end


# Installing Falcon

echo
echo "Installing Falcon"
yum clean all
rm -rf /var/cache/yum
dnf --nogpgcheck install falcon-sensor -y
/opt/CrowdStrike/falconctl -s --cid=6D26CF88945C4A5984CB190003B9370A-1E
systemctl start falcon-sensor

### end

# Doing yum update

echo "Doing a yum update"

yum update -y

### end

# This is the final check
clear
echo
echo
echo "Final verifications for Sat, Delinea Falcon"
echo
echo "Checking Sat registration"
subscription-manager list
echo
echo "Checking Delinea needs to comeback with Enabled and connected"
adinfo | grep 'Enabled\|connected'
echo
echo "Verify that falcon is installed"
rpm -qa | grep falcon
echo
echo "Verify that the falon-sensor service is running"
systemctl status falcon-sensor | grep running
echo
echo
echo "The postinstall.sh script has completed. Please reboot server at your convenience"
echo

### final end