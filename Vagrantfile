# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
 # The most common configuration options are documented and commented below.
 # For a complete reference, please see the online documentation at
 # https://docs.vagrantup.com.

 # Every Vagrant development environment requires a box. You can search for
 # boxes at https://vagrantcloud.com/search.
 config.vm.box = "ubuntu/bionic64"
 config.vm.box_version = "~> 20200304.0.0"
 # This pins the vm.box to a specific version so that it doesn't break if 
 # there are modifications made to the base image.
 
 config.vm.network "forwarded_port", guest: 8000, host: 8000
 # Maps a port from our local machine to the machine on our server so when we run our application on a network port 8000 and we want to make this port accessible from our host machine.
 # guest:8000 means port 8000 of our Local Development Server.
 
 # Below is the Provision Block where we can run scripts when we first create our server. I've added some commands to the script and the first one is to disable the auto update(line 33 & 34) which conflicts with this auto update(line 36) when we first run it. 

 # Next,I've added the update line here which will update the local repository with all of the available packages so that we can install Python 3 virtual env and zip Packages. We're going to be using these two packages later.  

 # Next, I create bash aliases file and I basically set Python 3 to the default Python version for our vagrant user. This just means that every time you run Python it will automatically use Python 3 and since we're using Python 3 in this course this just makes it handy because it means you don't need to type Python 3 manually every time you run a command.

 config.vm.provision "shell", inline: <<-SHELL
   systemctl disable apt-daily.service
   systemctl disable apt-daily.timer
 
   sudo apt-get update
   sudo apt-get install -y python3-venv zip
   touch /home/vagrant/.bash_aliases
   if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
     echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
     echo "alias python='python3'" >> /home/vagrant/.bash_aliases
   fi
 SHELL
end