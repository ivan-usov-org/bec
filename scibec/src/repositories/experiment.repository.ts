import { Getter, inject } from '@loopback/core';
import { HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { Experiment, ExperimentAccount, ExperimentRelations, Session } from '../models';
import { AutoAddRepository } from './autoadd.repository';
import { ExperimentAccountRepository } from './experiment-account.repository';
import { SessionRepository } from './session.repository';


export class ExperimentRepository extends AutoAddRepository<
  Experiment,
  typeof Experiment.prototype.id,
  ExperimentRelations
> {
  public readonly sessions: HasManyRepositoryFactory<Session, string>;
  public readonly experimentAccounts: HasManyRepositoryFactory<ExperimentAccount, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('ExperimentAccountRepository') sessionRepositoryGetter: Getter<SessionRepository>,
    @repository.getter('ExperimentAccountRepository') experimentAccountRepositoryGetter: Getter<ExperimentAccountRepository>,
  ) {
    super(Experiment, dataSource);
    this.sessions = this.createHasManyRepositoryFactoryFor('sessions', sessionRepositoryGetter);
    this.experimentAccounts = this.createHasManyRepositoryFactoryFor('experimentAccounts', experimentAccountRepositoryGetter);

    // add these lines to register inclusion resolver.
    this.registerInclusionResolver('sessions', this.sessions.inclusionResolver);
    this.registerInclusionResolver('experimentAccounts', this.experimentAccounts.inclusionResolver);
  }
}
