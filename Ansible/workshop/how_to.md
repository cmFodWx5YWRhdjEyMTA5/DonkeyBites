# Ansible workshop

### Vagrant 

The vagrant configuration will create 4 machines:
ansible (latest stable): 10.10.0.100
Prod Database: 10.10.0.101
Prod Frontend: 10.10.0.102
Dev: 10.10.0.110

user: user
password: qwe123

Each of the machines has only 512Mb ram so it can run also under older laptops, you may want to edit the vagrant file and change it to 1024Mb

### Use
Download the vagrant files from:

https://github.com/agmonr/Ansible/tree/master/vagrant

put the "Vagrant" and "bootstrap.sh" in a folder and run "vagrant up" to create and run the machines.

As long as the vagrant conintue to run, you can ignore the errors.

Login to the ansible machine (ssh user@10.10.0.100):

cd git/ansible/

ansible all -a "id" -k (provide password) (to check connectivity)

ansible-playbook servers.yml -k (provide password) (to activate ansible)

In case of failure, press Ctrl+c and try to re-run.

You may need to reboot all the machines, you can easily do it using:

ansible all -a "reboot" 
