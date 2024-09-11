# Competition

This is a proposal for a friendly competition between the participants.

The purpose of the game is to change the interface description of the Dell Sonic switch(es) based on the given words as fast as possible. This can be done by using various tools presented earlier

* CLI
    * netmiko
    * scrapli
    * paramiko
* restconf
* gnmi
* ansible
* nornir
* bash/curl


## Rules 

* each team selects a short plot of their favourite movie in 56 words, i.e the same number as interfaces on the Sonic switch.
    * the files for the movie plots are in the directory 'stories'
* you get points by changing the interface description to match the words in the plot of the movie you have selected
    * if you change the description to the same value as the current value, you get 0 points
    * if you change the description to some word which is not in the plot of the movie you have selected, you get 0 points
* interface number must match the number of the word in the plot of the movie you have selected
    * e.g if you sele the movie 'alien' which plot starts with words 'On a distant planet'
        * Ethernet 0 must have description 'On'
        * Ethernet 1 must have description 'a'
        * Ethernet 2 must have description 'distant'
        * Ethernet 3 must have description 'planet'
        * etc
    * please note that the device has interfaces 0-48, 52, 56, 60, 64, 68, 72, 76
* interface description can be only changed if the value is different that the value you are changing it to, i.e. only the changed description counts
    * the points are calculated with gnmi subscription with 'on_change'

ideas for optimisation:
* check which words are unique for your story and concentrate on changing only them
* check the current interface description and concentrate on changing only the words which are different from the current interface description
* optimise the number of used connections to the devices
* it is highly possible that devices under test will have significant load, write exception handling for the cases
* handle the secrets properly, do not hardcode them in the code

![points dashboard](image.png)