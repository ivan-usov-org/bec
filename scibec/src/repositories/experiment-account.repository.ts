import { inject } from '@loopback/core';
import { MongoDataSource } from '../datasources';
import { ExperimentAccount, ExperimentAccountRelations } from '../models/experiment-account.model';
import { AutoAddRepository } from './autoadd.repository';

export class ExperimentAccountRepository extends AutoAddRepository<
  ExperimentAccount,
  typeof ExperimentAccount.prototype.id,
  ExperimentAccountRelations
> {
  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
  ) {
    super(ExperimentAccount, dataSource);
  }
}
