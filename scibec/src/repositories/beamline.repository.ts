import { HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { Beamline, BeamlineRelations } from '../models';
import { Getter, inject } from '@loopback/core';
import { Session } from '../models';
import { SessionRepository } from './session.repository';
import { AutoAddRepository } from './autoadd.repository';


export class BeamlineRepository extends AutoAddRepository<
  Beamline,
  typeof Beamline.prototype.id,
  BeamlineRelations
> {
  public readonly sessions: HasManyRepositoryFactory<Session, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('SessionRepository') sessionRepositoryGetter: Getter<SessionRepository>,
  ) {
    super(Beamline, dataSource);
    this.sessions = this.createHasManyRepositoryFactoryFor('sessions', sessionRepositoryGetter);

    // add these lines to register inclusion resolver.
    this.registerInclusionResolver('sessions', this.sessions.inclusionResolver);
  }
}