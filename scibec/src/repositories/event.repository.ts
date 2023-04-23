import { inject } from '@loopback/core';
import { MongoDataSource } from '../datasources';
import { Event, EventRelations } from '../models';
import { AutoAddRepository } from './autoadd.repository';

export class EventRepository extends AutoAddRepository<
  Event,
  typeof Event.prototype.id,
  EventRelations
> {
  constructor(
    @inject('datasources.') dataSource: MongoDataSource,
  ) {
    super(Event, dataSource);
  }
}
