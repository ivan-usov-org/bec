import { Getter, inject } from '@loopback/core';
import { HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { Device, DeviceRelations, Event } from '../models';
import { AutoAddRepository } from './autoadd.repository';
import { EventRepository } from './event.repository';

export class DeviceRepository extends AutoAddRepository<
  Device,
  typeof Device.prototype.id,
  DeviceRelations
> {
  public readonly events: HasManyRepositoryFactory<Event, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('EventRepository') eventRepositoryGetter: Getter<EventRepository>,
  ) {
    super(Device, dataSource);
    this.events = this.createHasManyRepositoryFactoryFor('events', eventRepositoryGetter);

    this.registerInclusionResolver('events', this.events.inclusionResolver);

  }
}
