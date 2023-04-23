import { HasManyRepositoryFactory, HasOneRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { AccessConfig, Beamline, BeamlineRelations, Experiment } from '../models';
import { Getter, inject } from '@loopback/core';
import { AutoAddRepository } from './autoadd.repository';
import { ExperimentRepository } from './experiment.repository';
import { AccessConfigRepository } from './access-config.repository';


export class BeamlineRepository extends AutoAddRepository<
  Beamline,
  typeof Beamline.prototype.id,
  BeamlineRelations
> {
  public readonly experiments: HasManyRepositoryFactory<Experiment, string>;
  public readonly accessConfig: HasOneRepositoryFactory<AccessConfig, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('ExperimentRepository') experimentRepositoryGetter: Getter<ExperimentRepository>,
    @repository.getter('AccessConfigRepository') accessConfigRepositoryGetter: Getter<AccessConfigRepository>,
  ) {
    super(Beamline, dataSource);
    this.experiments = this.createHasManyRepositoryFactoryFor('experiments', experimentRepositoryGetter);
    this.accessConfig = this.createHasOneRepositoryFactoryFor('accessConfig', accessConfigRepositoryGetter);

    // add these lines to register inclusion resolver.
    this.registerInclusionResolver('experiments', this.experiments.inclusionResolver);
    this.registerInclusionResolver('accessConfig', this.accessConfig.inclusionResolver);
  }
}