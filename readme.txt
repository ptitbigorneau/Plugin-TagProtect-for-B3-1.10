# tagprotect plugin
# Plugin for B3 (www.bigbrotherbot.net)
# www.ptitbigorneau.fr

tagprotect plugin (v1.5) for B3

Requirements
------------

* BigBortherBot(3) >= version 1.10

Installation:
-------------

1. Copy the 'tagprotect' folder into 'b3/extplugins' and 'tagprotect.ini' file into '/b3/extplugins/conf'.

2. Open your B3.ini or b3.xml file (default in b3/conf) and add the next line in the [plugins] section of the file:
    for b3.xml
        <plugin name="tagprotect" config="@b3/extplugins/conf/tagprotect.ini"/>
    for b3.ini
        tagprotect: @b3/extplugins/conf/tagprotect.ini

3. Open tagprotect.ini

modify clan name (exemple : The Pirate Family )
modify tag exact (exemple : -[TPF]- )
modify second tag (exemple : -[TPF-T]- for test member by exemple)
modify approximate tag (exemple tpf )
modify pluginactived on/off
modify banactived yes/no

4. Run the contact SQL script (tagprotect.sql) on your B3 database
