import {Getter, inject} from '@loopback/core';
import {DefaultCrudRepository, HasManyRepositoryFactory, repository} from '@loopback/repository';
import {MongoDataSource} from '../datasources';
import {Device, Scan, Session, SessionRelations} from '../models';
import {DeviceRepository} from './device.repository';
import {ScanRepository} from './scan.repository';

export class SessionRepository extends DefaultCrudRepository<
  Session,
  typeof Session.prototype.id,
  SessionRelations
> {
  public readonly scans: HasManyRepositoryFactory<Scan, string>;
  public readonly devices: HasManyRepositoryFactory<Device, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('ScanRepository') scanRepositoryGetter: Getter<ScanRepository>,
    @repository.getter('DeviceRepository') deviceRepositoryGetter: Getter<DeviceRepository>
  ) {
    super(Session, dataSource);
    this.scans = this.createHasManyRepositoryFactoryFor('scans', scanRepositoryGetter);
    this.devices = this.createHasManyRepositoryFactoryFor('devices', deviceRepositoryGetter);


    // add these lines to register inclusion resolver.
    this.registerInclusionResolver('scans', this.scans.inclusionResolver);
    this.registerInclusionResolver('devices', this.devices.inclusionResolver);
  }
}
