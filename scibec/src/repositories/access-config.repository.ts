import { Getter, inject } from '@loopback/core';
import { HasManyRepositoryFactory, repository } from '@loopback/repository';
import { MongoDataSource } from '../datasources';
import { AccessConfig, AccessConfigRelations, FunctionalAccount } from '../models';
import { AutoAddRepository } from './autoadd.repository';
import { FunctionalAccountRepository } from './functional-account.repository';

export class AccessConfigRepository extends AutoAddRepository<
  AccessConfig,
  typeof AccessConfig.prototype.id,
  AccessConfigRelations
> {
  public readonly functionalAccounts: HasManyRepositoryFactory<FunctionalAccount, string>;

  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
    @repository.getter('FunctionalAccountRepository') functionalAccountRepositoryGetter: Getter<FunctionalAccountRepository>,
  ) {
    super(AccessConfig, dataSource);
    this.functionalAccounts = this.createHasManyRepositoryFactoryFor('functionalAccounts', functionalAccountRepositoryGetter);

    this.registerInclusionResolver('functionalAccounts', this.functionalAccounts.inclusionResolver);
  }
}
