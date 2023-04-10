import { Getter, inject } from '@loopback/core';
import { BelongsToAccessor, HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { Scan, ScanRelations, Session, Event } from '../models';
import { AutoAddRepository } from './autoadd.repository';
import { EventRepository } from './event.repository';
import { SessionRepository } from './session.repository';

export class ScanRepository extends AutoAddRepository<
  Scan,
  typeof Scan.prototype.id,
  ScanRelations
> {
  public readonly parent: BelongsToAccessor<Scan, any>;
  public readonly subscans: HasManyRepositoryFactory<Scan, string>;
  public readonly session: BelongsToAccessor<Session, string>;
  public readonly events: HasManyRepositoryFactory<Event, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('SessionRepository') sessionRepositoryGetter: Getter<SessionRepository>,
    @repository.getter('EventRepository') eventRepositoryGetter: Getter<EventRepository>
  ) {
    super(Scan, dataSource);
    this.subscans = this.createHasManyRepositoryFactoryFor('subscans', Getter.fromValue(this));
    this.parent = this.createBelongsToAccessorFor('parent', Getter.fromValue(this));
    this.session = this.createBelongsToAccessorFor('session', sessionRepositoryGetter);
    this.events = this.createHasManyRepositoryFactoryFor('events', eventRepositoryGetter);

    // add these lines to register inclusion resolver.
    this.registerInclusionResolver('subscans', this.subscans.inclusionResolver);
    this.registerInclusionResolver('parent', this.parent.inclusionResolver);
    this.registerInclusionResolver('session', this.session.inclusionResolver);
    this.registerInclusionResolver('events', this.events.inclusionResolver);

  }
}
