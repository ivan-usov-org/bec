import {inject, lifeCycleObserver, ValueOrPromise} from '@loopback/core';
import {AnyObject, juggler} from '@loopback/repository';

const config = {
  "name": "mongo",
  "connector": "mongodb",
  "url": "",
  "host": "localhost",
  "port": 27017,
  "user": "",
  "password": "",
  "database": "scibec",
  "useNewUrlParser": true,
  "useUnifiedTopology": true
}

function updateConfig(dsConfig: AnyObject) {
  return dsConfig;
}



@lifeCycleObserver('datasource')
export class MongoDataSource extends juggler.DataSource {
  static dataSourceName = 'mongo';

  constructor(
    @inject('datasources.config.mongo', {optional: true})
    dsConfig: AnyObject = config,
  ) {
    const fs = require('fs');
    let mongoConfig;
    if (fs.existsSync(process.env.CONFIGFILE)) {
      let config = JSON.parse(fs.readFileSync(process.env.CONFIGFILE, 'utf-8'));
      mongoConfig = config["mongodb"];
    } else {
      mongoConfig = dsConfig;
    }
    console.log(mongoConfig)
    super(updateConfig(mongoConfig));
  }

  /**
   * Disconnect the datasource when application is stopped. This allows the
   * application to be shut down gracefully.
   */
  stop(): ValueOrPromise<void> {
    return super.disconnect();
  }
}
