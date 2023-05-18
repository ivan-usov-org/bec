import { Getter, inject } from '@loopback/core';
import { HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { Dataset, DatasetRelations, Scan } from '../models';
import { ScanRepository } from './scan.repository';
import { AutoAddRepository } from './autoadd.repository';

export class DatasetRepository extends AutoAddRepository<
  Dataset,
  typeof Dataset.prototype.id,
  DatasetRelations
> {
  public readonly scans: HasManyRepositoryFactory<Scan, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('ScanRepository') scanRepositoryGetter: Getter<ScanRepository>,
  ) {
    super(Dataset, dataSource);
    this.scans = this.createHasManyRepositoryFactoryFor('scans', scanRepositoryGetter);

    this.registerInclusionResolver('scans', this.scans.inclusionResolver);
  }
}
