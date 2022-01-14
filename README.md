Shows the information of the observers from whom the information has been collected
==============

Getting Started
---------------

- Activate the ClimMob environment.
```
$ . ./path/to/ClimMob/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd dataCollectionProgressExtension
```

- Build the plugin
```
$ python setup.py develop
```

- Add the plugin to the ClimMob list of plugins by editing the following line in development.ini or production.ini
```
    #climmob.plugins = examplePlugin
    climmob.plugins = dataCollectionProgressExtension
```

- Run ClimMob again
