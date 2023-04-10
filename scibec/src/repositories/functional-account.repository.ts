import { inject } from '@loopback/core';
import { MongoDataSource } from '../datasources';
import { FunctionalAccount, FunctionalAccountRelations } from '../models/functional-account.model';
import { AutoAddRepository } from './autoadd.repository';

export class FunctionalAccountRepository extends AutoAddRepository<
  FunctionalAccount,
  typeof FunctionalAccount.prototype.id,
  FunctionalAccountRelations
> {
  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
  ) {
    super(FunctionalAccount, dataSource);
  }
}
